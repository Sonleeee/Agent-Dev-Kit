<#
.SYNOPSIS
    Agent-Dev-Kit Updater (adk update / adk up)
.DESCRIPTION
    Kiểm tra và cập nhật Agent-Dev-Kit lên phiên bản mới nhất.
    Đảm bảo an toàn 100%: KHÔNG BAO GIỜ ghi đè AGENTS.md và .agents/context/
#>
[CmdletBinding()]
param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   🔄 Agent-Dev-Kit Updater (adk up)      " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$CurrentDir = (Get-Location).Path
$TargetAgentsDir = Join-Path $CurrentDir ".agents"
$LocalKitPath = "C:\Sonlee\AI\Agent-Dev-Kit"
$RepoUrl = "https://github.com/Sonleeee/Agent-Dev-Kit.git"

# Kiểm tra thư mục .agents
if (-not (Test-Path $TargetAgentsDir)) {
    Write-Error "Dự án này chưa có thư mục .agents/. Hãy chạy install.ps1 trước!"
    return
}

# Đọc phiên bản hiện tại trong project
$LocalVersion = "0.0.0"
$LocalVersionFile = Join-Path $TargetAgentsDir "VERSION"
if (Test-Path $LocalVersionFile) {
    $LocalVersion = (Get-Content $LocalVersionFile -Raw).Trim()
}

Write-Host "📌 Phiên bản hiện tại trong project: v$LocalVersion" -ForegroundColor Gray

$TempDir = Join-Path ([System.IO.Path]::GetTempPath()) "adk-update-$(Get-Random)"
try {
    # 1. Tìm nguồn cập nhật mới nhất
    if (Test-Path $LocalKitPath) {
        Write-Host "📦 Kiểm tra bản cập nhật từ nguồn cục bộ: $LocalKitPath" -ForegroundColor Gray
        $SourcePath = $LocalKitPath
    } else {
        Write-Host "🌐 Đang kiểm tra bản cập nhật từ GitHub ($RepoUrl)..." -ForegroundColor Gray
        git clone --depth 1 $RepoUrl $TempDir --quiet
        $SourcePath = $TempDir
    }

    # Đọc phiên bản mới nhất từ source
    $RemoteVersion = "unknown"
    $RemoteVersionFile = Join-Path $SourcePath "VERSION"
    if (Test-Path $RemoteVersionFile) {
        $RemoteVersion = (Get-Content $RemoteVersionFile -Raw).Trim()
    }

    Write-Host "🔍 Phiên bản mới nhất: v$RemoteVersion" -ForegroundColor Gray

    # So sánh phiên bản
    if (($LocalVersion -eq $RemoteVersion) -and (-not $Force)) {
        Write-Host ""
        Write-Host "✅ Bạn đang sử dụng phiên bản mới nhất (v$LocalVersion). Không cần cập nhật!" -ForegroundColor Green
        Write-Host "   (Dùng cờ -Force nếu bạn muốn ép ghi đè/sửa chữa lại core files)" -ForegroundColor DarkGray
        return
    }

    Write-Host ""
    Write-Host "🚀 Đang cập nhật: v$LocalVersion -> v$RemoteVersion..." -ForegroundColor Cyan

    # Các thành phần Core được cập nhật
    $CoreItems = @(
        "workflows", "skills", "rules", "agents", "templates",
        "quality", "addons", "registry", "docs", "tools",
        "SYSTEM.md", "README.md", "CHANGELOG.md", "VERSION", "addon.ps1"
    )

    foreach ($item in $CoreItems) {
        $src = Join-Path $SourcePath $item
        if (Test-Path $src) {
            $dest = Join-Path $TargetAgentsDir $item
            Copy-Item -Path $src -Destination $dest -Recurse -Force
        }
    }

    Write-Host "🛡️  An toàn: Toàn bộ .agents/context/ và AGENTS.md được giữ nguyên 100%." -ForegroundColor Green
    Write-Host "🎉 Cập nhật thành công lên Agent-Dev-Kit v$RemoteVersion!" -ForegroundColor Green
}
finally {
    if (Test-Path $TempDir) {
        Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
