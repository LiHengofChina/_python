---
name: disk-alert-triage
description: 磁盘告警排查。磁盘满、df、空间不足、/var/log 过大、linux-231 磁盘问题、192.168.100.231 磁盘情况 时使用。
tools: ssh_exec, rag_search
host: 192.168.100.231
manual: ops_manual.txt
---

# 磁盘告警排查（linux-231）

## 触发条件
- 磁盘使用率 > 85%
- 用户问「231 磁盘为什么满」「怎么清理」

## 步骤（SOP）
1. ssh 连接 192.168.100.231
2. 执行 `df -h`，找出 >80% 的分区
3. 对异常分区执行 `du -sh /var/log/*`（手册优先查 /var/log），「根分区高则 du / 顶层目录」
4. 调用 rag_search，查询「磁盘空间告警处理」（来源：ops_manual.txt）
5. 汇总：根因 + 处理建议（logrotate / 压缩 / 扩容）
6. 若涉及 `rm -rf`、重启服务 → 只输出方案，末尾写「需人工审批」

## 手册要点（ops_manual.txt）
- 先 df -h，再 du 查 /var/log
- 禁止 rm 正在写入的日志；可 logrotate 或 truncate

## 验收清单
- [ ] 已给出占用最大的目录
- [ ] 建议与手册一致或有命令输出依据
- [ ] 危险操作未自动执行
