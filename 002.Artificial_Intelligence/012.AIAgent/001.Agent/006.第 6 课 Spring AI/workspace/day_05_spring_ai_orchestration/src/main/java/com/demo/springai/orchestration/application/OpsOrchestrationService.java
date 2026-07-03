package com.demo.springai.orchestration.application;

import com.demo.springai.orchestration.domain.model.OrchestrationContext;
import com.demo.springai.orchestration.domain.model.OrchestrationResult;
import com.demo.springai.orchestration.infrastructure.llm.IntentAnalyzer;
import com.demo.springai.orchestration.infrastructure.llm.OpsSynthesizer;
import com.demo.springai.orchestration.infrastructure.rag.ManualRagRetriever;
import com.demo.springai.orchestration.infrastructure.tool.ToolExecutionPlanner;
import org.springframework.stereotype.Service;

/**
 * Agent 编排器：用代码显式组织多步骤 / 多轮 LLM 调用。
 *
 * <p>与 day_04 对比：day_04 把 RAG+Tool 交给 Spring AI 黑盒调度；
 * 本课把每一步写清楚，便于生产里加审批、日志、重试。
 */
@Service
public class OpsOrchestrationService {

    private final IntentAnalyzer intentAnalyzer;
    private final ManualRagRetriever manualRagRetriever;
    private final ToolExecutionPlanner toolExecutionPlanner;
    private final OpsSynthesizer opsSynthesizer;

    public OpsOrchestrationService(
            IntentAnalyzer intentAnalyzer,
            ManualRagRetriever manualRagRetriever,
            ToolExecutionPlanner toolExecutionPlanner,
            OpsSynthesizer opsSynthesizer) {
        this.intentAnalyzer = intentAnalyzer;
        this.manualRagRetriever = manualRagRetriever;
        this.toolExecutionPlanner = toolExecutionPlanner;
        this.opsSynthesizer = opsSynthesizer;
    }

    /***

     就是普通的 Java 顺序调用：一步跑完再跑下一步，没有并行、没有框架魔法。

     每步产出基本都是 字符串（意图是枚举，记步骤时转成 intent.name()）
     中间结果放进 OrchestrationContext，供后面步骤用
     5 步全跑完后，打包成 OrchestrationResult 一次性返回

     */
    public OrchestrationResult run(String question) {
        OrchestrationContext ctx = new OrchestrationContext(question);

        // Step 1：意图识别（LLM 第 1 轮）
        var intent = intentAnalyzer.analyze(question);
        ctx.setIntent(intent);
        ctx.addStep(1, "意图识别", intent.name());

        // Step 2：RAG 检索（代码显式调用向量库，不用 Advisor）
        String manualExcerpt = manualRagRetriever.retrieve(question);
        ctx.setManualExcerpt(manualExcerpt);
        ctx.addStep(2, "RAG检索", truncate(manualExcerpt, 300));

        // Step 3：按意图执行 Tool（编排器决定调哪些命令，不是模型随意调）
        String toolOutputs = toolExecutionPlanner.execute(intent);
        ctx.setToolOutputs(toolOutputs);
        ctx.addStep(3, "现场采集", truncate(toolOutputs, 400));

        // Step 4：多轮推理 — 初稿 + 复核（LLM 第 2、3 轮）
        String draft = opsSynthesizer.draft(ctx);
        ctx.setDraftAnswer(draft);
        ctx.addStep(4, "推理-初稿", truncate(draft, 300));

        String finalAnswer = opsSynthesizer.refine(ctx);
        ctx.setFinalAnswer(finalAnswer);
        ctx.addStep(5, "推理-复核", finalAnswer);

        return new OrchestrationResult(question, ctx.getSteps(), finalAnswer);
    }

    private static String truncate(String text, int max) {
        if (text == null || text.length() <= max) {
            return text;
        }
        return text.substring(0, max) + "...";
    }
}
