<#
.SYNOPSIS
    Agent-Dev-Kit Installer (adk init)
.DESCRIPTION
    Khởi tạo Agent-Dev-Kit vào project hiện tại.
    Tự động chuẩn bị .agents/, AGENTS.md và bảo vệ context dự án.
#>
[CmdletBinding()]
param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   🤖 Agent-Dev-Kit Installer (adk)       " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$CurrentDir = (Get-Location).Path
$TargetAgentsDir = Join-Path $CurrentDir ".agents"
$LocalKitPath = "C:\Sonlee\AI\Agent-Dev-Kit"
$RepoUrl = "https://github.com/Sonleeee/Agent-Dev-Kit.git"

# Kiểm tra an toàn: Không chạy trong chính thư mục Agent-Dev-Kit gốc
if (Test-Path $LocalKitPath) {
    if ((Get-Item $CurrentDir).FullName -eq (Get-Item $LocalKitPath).FullName) {
        Write-Warning "Bạn đang đứng trong chính thư mục Agent-Dev-Kit gốc. Hãy chuyển sang thư mục project cần cài đặt!"
        return
    }
}

$TempDir = Join-Path ([System.IO.Path]::GetTempPath()) "adk-install-$(Get-Random)"
try {
    # 1. Tìm nguồn kit (ưu tiên thư mục local trên máy Sonlee nếu có, ngược lại kéo từ GitHub)
    if (Test-Path $LocalKitPath) {
        Write-Host "📦 Sử dụng nguồn Agent-Dev-Kit cục bộ: $LocalKitPath" -ForegroundColor Gray
        $SourcePath = $LocalKitPath
    } else {
        Write-Host "🌐 Đang tải Agent-Dev-Kit mới nhất từ GitHub ($RepoUrl)..." -ForegroundColor Gray
        git clone --depth 1 $RepoUrl $TempDir --quiet
        $SourcePath = $TempDir
    }

    # 2. Tạo thư mục .agents nếu chưa có
    if (-not (Test-Path $TargetAgentsDir)) {
        New-Item -ItemType Directory -Path $TargetAgentsDir -Force | Out-Null
        Write-Host "📁 Đã tạo thư mục .agents/" -ForegroundColor Green
    }

    # 3. Copy các thành phần Core
    $CoreItems = @(
        "workflows", "skills", "rules", "agents", "templates",
        "quality", "addons", "registry", "docs", "tools",
        "SYSTEM.md", "README.md", "CHANGELOG.md", "VERSION"
    )

    Write-Host "🚀 Đang sao chép các thành phần Core..." -ForegroundColor Gray
    foreach ($item in $CoreItems) {
        $src = Join-Path $SourcePath $item
        if (Test-Path $src) {
            $dest = Join-Path $TargetAgentsDir $item
            Copy-Item -Path $src -Destination $dest -Recurse -Force
        }
    }

    # 4. Khởi tạo Context cho project (nếu chưa có)
    $TargetContextDir = Join-Path $TargetAgentsDir "context"
    if (-not (Test-Path $TargetContextDir)) {
        New-Item -ItemType Directory -Path $TargetContextDir -Force | Out-Null
        $TemplateContext = Join-Path $SourcePath "_project-template\.agents\context\*"
        if (Test-Path $TemplateContext) {
            Copy-Item -Path $TemplateContext -Destination $TargetContextDir -Recurse -Force
        }
        Write-Host "📝 Đã tạo khung context tại .agents/context/" -ForegroundColor Green
    } else {
        Write-Host "ℹ️  Thư mục .agents/context/ đã có sẵn, giữ nguyên an toàn." -ForegroundColor Yellow
    }

    # 5. Tạo AGENTS.md tại root (nếu chưa có)
    $AgentsFile = Join-Path $CurrentDir "AGENTS.md"
    if (-not (Test-Path $AgentsFile)) {
        $TemplateAgents = Join-Path $SourcePath "_project-template\AGENTS.md"
        if (Test-Path $TemplateAgents) {
            Copy-Item -Path $TemplateAgents -Destination $AgentsFile -Force
            Write-Host "📄 Đã tạo AGENTS.md tại thư mục gốc" -ForegroundColor Green
        }
    } else {
        Write-Host "ℹ️  AGENTS.md đã có sẵn, giữ nguyên an toàn." -ForegroundColor Yellow
    }

    # 6. Thêm .agents vào .gitignore nếu có git
    $GitIgnoreFile = Join-Path $CurrentDir ".gitignore"
    if (Test-Path $GitIgnoreFile) {
        $giContent = Get-Content $GitIgnoreFile -Raw -ErrorAction SilentlyContinue
        if ($giContent -notmatch "(?m)^\.agents/?$") {
            Add-Content -Path $GitIgnoreFile -Value "`n.agents/"
            Write-Host "🔒 Đã thêm .agents/ vào .gitignore" -ForegroundColor Green
        }
    }

    # 7. Tự động đăng ký lệnh 'adk' vào PowerShell Profile (để gõ được ở mọi nơi)
    try {
        if ($PROFILE) {
            $profileDir = Split-Path -Parent $PROFILE
            if (-not (Test-Path $profileDir)) {
                New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
            }
            if (-not (Test-Path $PROFILE)) {
                New-Item -ItemType File -Path $PROFILE -Force | Out-Null
            }

            $profileContent = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue
            if ($profileContent -notmatch "function\s+adk\b") {
                $adkSnippet = @'

# --- Agent-Dev-Kit CLI (adk) ---
function adk {
    param([string]$cmd = "init", [switch]$Force)
    $localKit = "C:\Sonlee\AI\Agent-Dev-Kit"
    $remoteRepo = "https://raw.githubusercontent.com/Sonleeee/Agent-Dev-Kit/main"
    $runLocal = Test-Path $localKit

    switch ($cmd.ToLower()) {
        { $_ -in "i", "init", "install" } {
            if ($runLocal) { & "$localKit\install.ps1" -Force:$Force }
            else { irm "$remoteRepo/install.ps1" | iex }
        }
        { $_ -in "up", "update" } {
            if ($runLocal) { & "$localKit\update.ps1" -Force:$Force }
            else { irm "$remoteRepo/update.ps1" | iex }
        }
        { $_ -in "v", "ver", "version", "-v", "--version" } {
            $ver = "unknown"
            if (Test-Path ".agents\VERSION") { $ver = (Get-Content ".agents\VERSION" -Raw).Trim() }
            elseif ($runLocal -and (Test-Path "$localKit\VERSION")) { $ver = (Get-Content "$localKit\VERSION" -Raw).Trim() }
            Write-Host "🤖 Agent-Dev-Kit v$ver" -ForegroundColor Cyan
        }
        { $_ -in "help", "-h", "--help" } {
            Write-Host "==========================================" -ForegroundColor Cyan
            Write-Host "   🤖 Agent-Dev-Kit CLI (adk)             " -ForegroundColor Cyan
            Write-Host "==========================================" -ForegroundColor Cyan
            Write-Host "  adk, adk i, adk install : Khởi tạo kit cho project" -ForegroundColor Gray
            Write-Host "  adk up, adk update      : Cập nhật kit lên bản mới nhất" -ForegroundColor Gray
            Write-Host "  adk version, adk -v     : Xem phiên bản hiện tại" -ForegroundColor Gray
        }
        default {
            if ($runLocal) { & "$localKit\install.ps1" -Force:$Force }
            else { irm "$remoteRepo/install.ps1" | iex }
        }
    }
}
'@
                Add-Content -Path $PROFILE -Value $adkSnippet -Encoding utf8
                Write-Host "⚡ Đã tự động đăng ký lệnh 'adk' vào PowerShell Profile!" -ForegroundColor Green
            }

            # Nạp ngay function adk vào phiên hiện tại để dùng được luôn
            Set-Item -Path function:global:adk -Value {
                param([string]$cmd = "init", [switch]$Force)
                $localKit = "C:\Sonlee\AI\Agent-Dev-Kit"
                $remoteRepo = "https://raw.githubusercontent.com/Sonleeee/Agent-Dev-Kit/main"
                $runLocal = Test-Path $localKit

                switch ($cmd.ToLower()) {
                    { $_ -in "i", "init", "install" } {
                        if ($runLocal) { & "$localKit\install.ps1" -Force:$Force }
                        else { irm "$remoteRepo/install.ps1" | iex }
                    }
                    { $_ -in "up", "update" } {
                        if ($runLocal) { & "$localKit\update.ps1" -Force:$Force }
                        else { irm "$remoteRepo/update.ps1" | iex }
                    }
                    { $_ -in "v", "ver", "version", "-v", "--version" } {
                        $ver = "unknown"
                        if (Test-Path ".agents\VERSION") { $ver = (Get-Content ".agents\VERSION" -Raw).Trim() }
                        elseif ($runLocal -and (Test-Path "$localKit\VERSION")) { $ver = (Get-Content "$localKit\VERSION" -Raw).Trim() }
                        Write-Host "🤖 Agent-Dev-Kit v$ver" -ForegroundColor Cyan
                    }
                    { $_ -in "help", "-h", "--help" } {
                        Write-Host "==========================================" -ForegroundColor Cyan
                        Write-Host "   🤖 Agent-Dev-Kit CLI (adk)             " -ForegroundColor Cyan
                        Write-Host "==========================================" -ForegroundColor Cyan
                        Write-Host "  adk, adk i, adk install : Khởi tạo kit cho project" -ForegroundColor Gray
                        Write-Host "  adk up, adk update      : Cập nhật kit lên bản mới nhất" -ForegroundColor Gray
                        Write-Host "  adk version, adk -v     : Xem phiên bản hiện tại" -ForegroundColor Gray
                    }
                    default {
                        if ($runLocal) { & "$localKit\install.ps1" -Force:$Force }
                        else { irm "$remoteRepo/install.ps1" | iex }
                    }
                }
            }
        }
    } catch {
        Write-Verbose "Không thể tự động cập nhật profile: $_"
    }

    $InstalledVersion = "unknown"
    $VersionFile = Join-Path $TargetAgentsDir "VERSION"
    if (Test-Path $VersionFile) {
        $InstalledVersion = (Get-Content $VersionFile -Raw).Trim()
    }

    Write-Host ""
    Write-Host "✨ Khởi tạo thành công Agent-Dev-Kit (v$InstalledVersion)!" -ForegroundColor Green
    Write-Host "💡 Từ giờ, bạn chỉ cần gõ 'adk' (cài mới) hoặc 'adk up' (cập nhật) ở bất kỳ đâu!" -ForegroundColor Cyan
    Write-Host "👉 Bước tiếp theo: Mở file AGENTS.md để điền thông tin dự án." -ForegroundColor Yellow
}
finally {
    if (Test-Path $TempDir) {
        Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
