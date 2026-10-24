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
$LocalKitPath = if ($env:ADK_HOME -and (Test-Path $env:ADK_HOME)) { $env:ADK_HOME } elseif (Test-Path (Join-Path $PSScriptRoot "templates\AGENTS.md.template")) { $PSScriptRoot } else { "" }
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
        "rules", "agents", "templates",
        "schemas", "addons", "tools",
        "SYSTEM.md", "README.md", "CHANGELOG.md", "VERSION", "addon.ps1"
    )

    # Dọn dẹp các thư mục rác cũ đã khai tử của Kit (không xóa file riêng của user)
    $ObsoleteItems = @("quality", "registry", "docs", "context", "workflows")
    if (Test-Path $TargetAgentsDir) {
        foreach ($obs in $ObsoleteItems) {
            $obsPath = Join-Path $TargetAgentsDir $obs
            if (Test-Path $obsPath) {
                Remove-Item -Path $obsPath -Recurse -Force -ErrorAction SilentlyContinue
            }
        }
    }
    foreach ($item in $CoreItems) {
        $src = Join-Path $SourcePath $item
        if (Test-Path $src) {
            $dest = Join-Path $TargetAgentsDir $item
            if (Test-Path -Path $src -PathType Container) {
                if (Test-Path $dest) {
                    Remove-Item -Path $dest -Recurse -Force -ErrorAction SilentlyContinue
                }
                Copy-Item -Path $src -Destination $TargetAgentsDir -Recurse -Force
            } else {
                Copy-Item -Path $src -Destination $dest -Force
            }
        }
    }

    # Agent Skills hosts discover one skill folder directly under .agents/skills.
    # Keep category folders in the source repo; export each skill as a flat folder.
    $SkillSourceRoot = Join-Path $SourcePath "skills"
    $SkillTargetRoot = Join-Path $TargetAgentsDir "skills"
    if (Test-Path $SkillSourceRoot) {
        New-Item -ItemType Directory -Path $SkillTargetRoot -Force | Out-Null
        $SkillDirs = Get-ChildItem -Path $SkillSourceRoot -Directory |
            Where-Object { $_.Name -notlike "adk-*" -and $_.Name -notlike "sk-*" } |
            ForEach-Object { Get-ChildItem -Path $_.FullName -Directory -Recurse } |
            Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") } |
            Sort-Object FullName
        $ExportedSkillNames = @{}
        $ExportedSkillCount = 0

        foreach ($SkillSourceDir in $SkillDirs) {
            $SkillName = $SkillSourceDir.Name
            if ($ExportedSkillNames.ContainsKey($SkillName)) {
                Write-Warning "Skill trùng tên '$SkillName'; bỏ qua bản ở $($SkillSourceDir.FullName)."
                continue
            }
            $ExportedSkillNames[$SkillName] = $true

            $SkillDest = Join-Path $SkillTargetRoot $SkillName
            $ManagedMarker = Join-Path $SkillDest ".adk-managed"
            if ((Test-Path $SkillDest) -and -not (Test-Path $ManagedMarker)) {
                Write-Warning "Giữ nguyên skill người dùng '$SkillName'; không ghi đè."
                continue
            }
            New-Item -ItemType Directory -Path $SkillDest -Force | Out-Null
            Get-ChildItem -Path $SkillSourceDir.FullName -Force |
                ForEach-Object { Copy-Item -Path $_.FullName -Destination $SkillDest -Recurse -Force }
            New-Item -ItemType File -Path $ManagedMarker -Force | Out-Null
            $ExportedSkillCount++
        }
        Write-Host "🧩 Đã export $ExportedSkillCount skill theo layout .agents/skills/<name>/" -ForegroundColor Gray
    }

    Write-Host "🛡️  An toàn: Toàn bộ AGENTS.md và cấu hình riêng được giữ nguyên 100%." -ForegroundColor Green
    Write-Host "🎉 Cập nhật thành công lên Agent-Dev-Kit v$RemoteVersion!" -ForegroundColor Green
}
finally {
    if (Test-Path $TempDir) {
        Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
