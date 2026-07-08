$env:PATH = "D:\ProgramFiles\nodejs;" + $env:PATH
$allowDir = "D:/"
$port = 8106
$lanIp = "127.0.0.1"

Write-Host "[Day07-02] port=$port allow_dir=$allowDir"
Write-Host "[Day07-02] agent url: http://${lanIp}:$port"

& "D:\ProgramFiles\nodejs\npx.cmd" -y supergateway `
  --stdio "D:\ProgramFiles\nodejs\npx.cmd -y @modelcontextprotocol/server-filesystem@2026.1.14 $allowDir" `
  --port $port `
  --baseUrl "http://${lanIp}:$port" `
  --ssePath /sse `
  --messagePath /message
