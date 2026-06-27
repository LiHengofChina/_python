# -*- coding: utf-8 -*-
"""
================================================================================
day_29 — 最简单的 Python RAG Demo
================================================================================

RAG = Retrieval-Augmented Generation（检索增强生成）

"""

import os
import re
from pathlib import Path

import jieba
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def jieba_tokenizer(text: str) -> list[str]:
    """中文分词后再做 TF-IDF，检索效果比按字切分更好。"""
    return list(jieba.cut(text))


# =============================================================================
# 【0】配置
# =============================================================================

# 示例运维手册路径（RAG 的「知识库」来源）
DOC_PATH = Path(__file__).parent / "data" / "ops_manual.txt"

# 切块参数：块越大上下文越完整，但检索越不精准；块越小反之
CHUNK_SIZE = 200          # 每块大约多少字符（中文按字符计）
CHUNK_OVERLAP = 40        # 相邻块重叠字符数，避免一句话被拦腰截断

# 检索参数：取相似度最高的前 K 个块拼进 Prompt
TOP_K = 2

# 是否调用真实大模型（需本机 Ollama 等 OpenAI 兼容服务）
USE_LLM = os.environ.get("USE_LLM", "0") == "1"
LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "http://127.0.0.1:11434/v1")
LLM_MODEL = os.environ.get("LLM_MODEL", "qwen2.5:7b")


# =============================================================================
# 【1】加载文档
# =============================================================================

def load_document(path: Path) -> str:
    """
    读取原始文档全文。

    RAG 的知识可以来自：txt、Markdown、PDF 解析结果、数据库导出等。
    本 Demo 使用一份运维手册文本。
    """
    text = path.read_text(encoding="utf-8")
    print(f"[1] 已加载文档：{path.name}，共 {len(text)} 字符")
    return text


# =============================================================================
# 【2】文档切块（Chunking）
# =============================================================================

def split_by_sections(text: str) -> list[str]:
    """
    优先按 Markdown 二级标题（##）切分，保证每块语义相对完整。

    若文档没有标题，可改用 split_by_fixed_size() 固定长度滑动窗口切分。
    """
    # 按 "## " 分段，去掉空段
    parts = re.split(r"\n(?=## )", text.strip())
    chunks = [p.strip() for p in parts if p.strip()]
    return chunks


def split_by_fixed_size(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    固定长度 + 重叠窗口切分（当文档没有明显章节时使用）。

    例：chunk_size=200, overlap=40
        块1: 字符 0~200
        块2: 字符 160~360  （与块1 重叠 40 字符）
    """
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunks.append(text[start:end].strip())
        if end >= text_len:
            break
        start += chunk_size - overlap
    return [c for c in chunks if c]


def build_chunks(text: str) -> list[str]:
    """组合策略：有章节则按章节，否则按固定长度。"""
    if "## " in text:
        chunks = split_by_sections(text)
        print(f"[2] 按「## 标题」切块，共 {len(chunks)} 块")
    else:
        chunks = split_by_fixed_size(text, CHUNK_SIZE, CHUNK_OVERLAP)
        print(f"[2] 按固定长度切块，共 {len(chunks)} 块")

    for i, c in enumerate(chunks):
        preview = c.replace("\n", " ")[:60]
        print(f"    块{i}: {preview}...")
    return chunks


# =============================================================================
# 【3】向量化 + 「向量库」（本 Demo：TF-IDF 矩阵 + 内存存储）
# =============================================================================

class SimpleVectorStore:
    """
    最小向量库：把每个 chunk 变成向量，支持按相似度检索。

    生产环境常见：Chroma、Milvus、PGVector、Elasticsearch 等。
    本类用 sklearn 的 TfidfVectorizer 把文本变成稀疏向量，存在内存里。

    【和 Embedding 的区别】
    - TF-IDF：词频统计，「关键词重合」即相似（如「磁盘」「日志」同时出现）
    - Embedding：神经网络语义向量，「意思相近」即相似（如「磁盘满」≈「空间不足」）
    """

    def __init__(self):
        # token_pattern=None：配合自定义 tokenizer 处理中文
        self.vectorizer = TfidfVectorizer(tokenizer=jieba_tokenizer, token_pattern=None)
        self.chunks: list[str] = []
        self.matrix = None  # shape: (块数, 特征维度)

    def add_documents(self, chunks: list[str]) -> None:
        """入库：对所有块做 TF-IDF 向量化。"""
        self.chunks = chunks
        self.matrix = self.vectorizer.fit_transform(chunks)
        print(f"[3] 已向量化入库：{self.matrix.shape[0]} 块，"
              f"特征维度 {self.matrix.shape[1]}")

    def search(self, query: str, top_k: int = TOP_K) -> list[tuple[int, float, str]]:
        """
        检索：把用户问题也向量化，与库中每块算余弦相似度，取 Top-K。

        返回：[(块下标, 相似度分数, 块文本), ...]
        """
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix)[0]

        # 按分数从高到低排序，取前 top_k
        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for idx in top_indices:
            results.append((int(idx), float(scores[idx]), self.chunks[idx]))
        return results


# =============================================================================
# 【4】拼装 Prompt（检索结果 + 用户问题）
# =============================================================================

def build_rag_prompt(question: str, retrieved: list[tuple[int, float, str]]) -> str:
    """
    RAG 的核心 Prompt 模板：

    把「检索到的参考资料」和「用户问题」一起交给大模型，
    并明确要求：只根据资料回答，避免胡编（减轻幻觉）。
    """
    context_parts = []
    for rank, (idx, score, text) in enumerate(retrieved, start=1):
        context_parts.append(f"--- 资料{rank}（块{idx}，相似度 {score:.4f}）---\n{text}")

    context = "\n\n".join(context_parts)

    prompt = f"""你是银行运维助手。请严格根据以下参考资料回答问题。
若资料中没有相关内容，请明确回答「资料中未找到，无法确定」。

【参考资料】
{context}

【用户问题】
{question}

【回答】
"""
    return prompt


# =============================================================================
# 【5】生成答案（Generator）
# =============================================================================

def generate_mock(question: str, retrieved: list[tuple[int, float, str]]) -> str:
    """
    Mock 生成：不调用大模型，直接展示 RAG 检索到了什么。

    学习阶段建议先看懂检索结果是否合理，再接入真实 LLM。
    """
    lines = [
        "【Mock 模式】未调用大模型，以下为根据检索资料整理的要点：",
        f"您的问题：{question}",
        "",
        "检索到的相关内容：",
    ]
    for rank, (idx, score, text) in enumerate(retrieved, start=1):
        lines.append(f"  ({rank}) 相似度 {score:.4f}：")
        # 只取每块前 3 行，避免输出过长
        for line in text.splitlines()[:5]:
            if line.strip():
                lines.append(f"      {line.strip()}")
        lines.append("")
    lines.append("提示：设置环境变量 USE_LLM=1 且本机 Ollama 运行时，可改为真实大模型生成。")
    return "\n".join(lines)


def generate_llm(prompt: str) -> str:
    """
    调用 OpenAI 兼容 API 生成答案（Ollama / vLLM / 各类国产大模型网关均可）。

    示例（Ollama）：
        set USE_LLM=1
        set LLM_BASE_URL=http://127.0.0.1:11434/v1
        set LLM_MODEL=qwen2.5:7b
        python 01_rag_demo.py
    """
    try:
        from openai import OpenAI
    except ImportError:
        return "未安装 openai 包，请执行：pip install openai"

    client = OpenAI(base_url=LLM_BASE_URL, api_key="ollama")  # Ollama 不校验 key
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


# =============================================================================
# 【6】主流程：串起 RAG 五步
# =============================================================================

def rag_answer(question: str, store: SimpleVectorStore) -> None:
    """对单个问题执行完整 RAG 流程并打印结果。"""

    print("\n" + "=" * 70)
    print(f"用户问题：{question}")
    print("=" * 70)

    # ④ 检索
    retrieved = store.search(question, top_k=TOP_K)
    print(f"\n[4] 检索 Top-{TOP_K}：")
    for rank, (idx, score, text) in enumerate(retrieved, start=1):
        print(f"    Top{rank} | 块{idx} | 相似度 {score:.4f} | {text[:50].replace(chr(10), ' ')}...")

    # ⑤ 拼 Prompt + 生成
    prompt = build_rag_prompt(question, retrieved)
    print(f"\n[5] 已拼装 Prompt（长度 {len(prompt)} 字符）")
    print("-" * 40 + " Prompt 预览 " + "-" * 40)
    print(prompt[:800] + ("..." if len(prompt) > 800 else ""))
    print("-" * 88)

    if USE_LLM:
        print("\n[5] 调用大模型生成...")
        answer = generate_llm(prompt)
    else:
        print("\n[5] Mock 生成（未调用大模型）...")
        answer = generate_mock(question, retrieved)

    print("\n【最终回答】")
    print(answer)


def main():
    print("=" * 70)
    print("day_29 — Python RAG Demo（检索增强生成）")
    print("=" * 70)

    # ① 加载
    text = load_document(DOC_PATH)

    # ② 切块
    chunks = build_chunks(text)

    # ③ 向量化入库
    store = SimpleVectorStore()
    store.add_documents(chunks)


    # 演示：问两个运维相关问题
    print("\n" + "-" * 70 + "\n")
    demo_questions = [
        # "磁盘使用率超过 85% 应该怎么处理？",
        # "Nginx 返回 502 怎么排查？",
        "数据库连接数过多怎么办？",
    ]


    for q in demo_questions:
        print("\n" + "-" * 70 + "\n" )
        rag_answer(q, store)

    print("\n" + "-" * 70 + "\n")
    print("Demo 结束。建议对照注释理解：切块 → 向量库 → 检索 → Prompt → 生成。")
    print("=" * 70)


if __name__ == "__main__":
    main()
