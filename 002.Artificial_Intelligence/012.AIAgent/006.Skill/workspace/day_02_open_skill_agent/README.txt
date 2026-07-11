day_02_open_skill_agent — 调用开源 Skill（OpenOcta MySQL数据库巡检）

Skill：../../skills/openocta/mysql_inspect/SKILL.md
适配：../../skills/openocta/mysql_inspect/adapter.yaml

步骤：
  1) Skill 已从 GitHub 下载到 skills/openocta/mysql_inspect/
  2) copy config.example.yml → config.local.yml，填写 mysql 连接
  3) pip install -r requirements.txt
  4) python main.py "对 MySQL 做一次全维度健康巡检"

与 day_01 的区别：
  - 开源 Skill 原文不改，用 adapter.yaml 声明 tools
  - Tool 是 mysql_inspect_run，封装 scripts/mysql_inspect/*.py
  - 密码在 config.local.yml，不交给大模型

可选模块（未配置可跳过）：
  - Prometheus：需 prometheus.url
  - 飞书推送：需 feishu.webhook_url
