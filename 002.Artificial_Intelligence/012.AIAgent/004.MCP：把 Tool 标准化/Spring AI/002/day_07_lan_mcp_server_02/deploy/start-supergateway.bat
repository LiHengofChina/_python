@echo off
setlocal EnableExtensions

set "NODE_HOME=D:\ProgramFiles\nodejs"
set "PATH=%NODE_HOME%;%PATH%"

set "ALLOW_DIR=D:/"
set "PORT=8106"
set "LAN_IP=127.0.0.1"

echo [Day07-02] port=%PORT% allow_dir=%ALLOW_DIR%
echo [Day07-02] agent url: http://%LAN_IP%:%PORT%

npx -y supergateway --stdio "%NODE_HOME%\npx.cmd -y @modelcontextprotocol/server-filesystem@2026.1.14 %ALLOW_DIR%" --port %PORT% --baseUrl http://%LAN_IP%:%PORT% --ssePath /sse --messagePath /message
