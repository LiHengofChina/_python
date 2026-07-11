day_03_oracle_skill_agent — 调用 Oracle 官方 Skill（oracle/skills db 域）

Skill：../../skills/oracle/db/SKILL.md
适配：../../skills/oracle/db/adapter.yaml

与 day_02 MySQL 的区别：
  - MySQL（openocta）：自带 scripts/*.py，Tool 直接跑脚本
  - Oracle（官方）：路由 SKILL.md + 子文档 md，Tool 按需读取 + 可选 SQL

步骤：
  1) db 域已下载到 skills/oracle/db/
  2) copy config.example.yml → config.local.yml
  3) pip install -r requirements.txt
  4) python main.py "你的问题"

无 Oracle 库时：仍可跑，Agent 会用 oracle_skill_read 读 SOP 给定位思路；
  要查真实数据：oracle.enabled=true + 配好连接（或 use_ssh_exec + 服务器 sqlplus）。

Oracle 11g 注意：
  - thin 模式不支持，需本目录 instantclient/instantclient_19_26（已配置 instant_client_dir）
  - 首次使用请确认 instantclient 已解压到上述目录

当前测试库（已探测）：
  当前使用 192.168.35.13 bbed / test03（稳定可用）
  备选 192.168.35.25 TEST2 / lg_user（213 张表，目前 ORA-28547 连不上）
  勿用 192.168.100.50 prod / sys SYSDBA（生产库）

运行示例：
  python main.py "Oracle 有一条 SQL 很慢，帮我定位"
  python main.py "怎么查 alert log 和 top SQL"
  python main.py "会话阻塞怎么排查"
