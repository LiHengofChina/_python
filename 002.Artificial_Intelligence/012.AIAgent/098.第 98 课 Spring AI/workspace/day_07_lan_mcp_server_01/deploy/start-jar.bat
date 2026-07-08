@echo off
chcp 65001 >nul
setlocal

rem Day07 自研 MCP：外网 mvn package，内网 java -jar

set JAR=target\day07-lan-mcp-server-01-1.0.0.jar
set PORT=8104

if not exist "%JAR%" (
  echo [错误] 找不到 %JAR%，请先在本工程执行 mvn package
  pause
  exit /b 1
)

echo [Day07-01] 启动自研 MCP Server，端口 %PORT%
echo Agent 配置：sse.connections.ops-server.url=http://本机内网IP:%PORT%
java -jar "%JAR%" --server.port=%PORT%
