day_01_skill_agent — LangChain + LangGraph + 自研 Skill

Skill 文件：../../skills/disk_alert/SKILL.md

运行：
  cd workspace/day_01_skill_agent
  pip install -r requirements.txt
  copy config.example.yml config.local.yml
  python main.py "linux-231 磁盘满了"

注意：
  Ollama 需 ollama serve + qwen2.5:7b
  agent.py 已设 client_kwargs trust_env=False（避免 httpx 走代理 502）
  config.local.yml 勿提交 Git
