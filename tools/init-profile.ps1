<#
.SYNOPSIS
    Khoi tao hoac chinh sua Global Developer Profile (~/.agents/developer.md)
#>
[CmdletBinding()]
param()

$GlobalAgentsDir = Join-Path $env:USERPROFILE ".agents"
if (-not (Test-Path $GlobalAgentsDir)) {
    New-Item -ItemType Directory -Path $GlobalAgentsDir -Force | Out-Null
}

$ProfilePath = Join-Path $GlobalAgentsDir "developer.md"
$TemplatePath = Join-Path (Split-Path -Parent $PSScriptRoot) "templates\developer.md.template"

if (-not (Test-Path $ProfilePath)) {
    if (Test-Path $TemplatePath) {
        Copy-Item -Path $TemplatePath -Destination $ProfilePath -Force
        Write-Host "Da tao moi Global Developer Profile tai: $ProfilePath" -ForegroundColor Green
    } else {
        Write-Host "Khong tim thay template tai: $TemplatePath" -ForegroundColor Yellow
    }
} else {
    Write-Host "Global Developer Profile da ton tai tai: $ProfilePath" -ForegroundColor Cyan
}

Write-Host "Ban co the chinh sua file nay de ap dung gu code cho moi du an tren may!" -ForegroundColor Yellow
