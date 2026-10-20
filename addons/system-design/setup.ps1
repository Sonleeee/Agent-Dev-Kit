[CmdletBinding()]
param()

$ScriptDir = $PSScriptRoot
$SetupJs = Join-Path $ScriptDir "setup.js"

if (Test-Path $SetupJs) {
    node $SetupJs
} else {
    Write-Error "Không tìm thấy setup.js tại: $SetupJs"
}
