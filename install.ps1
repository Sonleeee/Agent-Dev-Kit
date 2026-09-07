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
        "SYSTEM.md", "README.md", "CHANGELOG.md", "VERSION", "addon.ps1"
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
    param(
        [string]$cmd = "init",
        [string]$subcmd = "",
        [switch]$Force
    )
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
        { $_ -in "addon", "addons" } {
            if ($runLocal -and (Test-Path "$localKit\addon.ps1")) {
                & "$localKit\addon.ps1" $subcmd $args
            } elseif (Test-Path ".agents\addon.ps1") {
                & ".\.agents\addon.ps1" $subcmd $args
            } else {
                irm "$remoteRepo/addon.ps1" | iex
            }
        }
        { $_ -in "v", "ver", "version", "-v", "--version" } {
            $ver = "unknown"
            if (Test-Path ".agents\VERSION") { $ver = (Get-Content ".agents\VERSION" -Raw).Trim() }
            elseif ($runLocal -and (Test-Path "$localKit\VERSION")) { $ver = (Get-Content "$localKit\VERSION" -Raw).Trim() }
            Write-Host "🤖 Agent-Dev-Kit v$ver" -ForegroundColor Cyan
        }
        { $_ -in "help", "-h", "--help" } {
            Write-Host ""
            Write-Host "========================================================================" -ForegroundColor Cyan
            Write-Host "   🤖 AGENT-DEV-KIT CLI (adk) — Hướng Dẫn Sử Dụng                       " -ForegroundColor Cyan
            Write-Host "========================================================================" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "📌 1. LỆNH CLI CƠ BẢN:" -ForegroundColor Yellow
            Write-Host "  adk, adk i, adk install   : Khởi tạo kit vào project (.agents/)" -ForegroundColor White
            Write-Host "  adk up, adk update        : Cập nhật core kit lên bản mới nhất" -ForegroundColor White
            Write-Host "  adk addon [tên]           : Quản lý, xem link và cài đặt addons" -ForegroundColor White
            Write-Host "  adk version, adk -v       : Xem phiên bản hiện tại" -ForegroundColor White
            Write-Host "  adk help, adk --help      : Xem bảng trợ giúp này" -ForegroundColor White
            Write-Host ""
            Write-Host "💬 2. CÁCH DÙNG TRONG CHAT (WORKFLOWS):" -ForegroundColor Yellow
            Write-Host "  /wf-scout                 : Khảo sát, đọc hiểu codebase dự án" -ForegroundColor White
            Write-Host "  /wf-plan <tính năng>     : Lên kế hoạch chi tiết trước khi code" -ForegroundColor White
            Write-Host "  /wf-cook                  : Triển khai code bám sát plan đã duyệt" -ForegroundColor White
            Write-Host "  /wf-fix <lỗi>             : Chẩn đoán và sửa lỗi theo quy trình" -ForegroundColor White
            Write-Host "  /wf-test                  : Sinh unit test và kịch bản kiểm thử" -ForegroundColor White
            Write-Host "  /wf-review                : Rà soát chất lượng code và regression" -ForegroundColor White
            Write-Host ""
            Write-Host "📦 3. DANH SÁCH 6 ADDONS (Gõ 'adk addon' để chọn và cài đặt):" -ForegroundColor Yellow
            Write-Host "  • archify    : Vẽ sơ đồ HTML tương tác (https://vividkit.dev/vi/guides/archify)" -ForegroundColor Gray
            Write-Host "  • database   : Tra cứu schema & query an toàn qua Gridex MCP" -ForegroundColor Gray
            Write-Host "  • obsidian   : Đồng bộ tri thức hai chiều với Second Brain (https://obsidian.md)" -ForegroundColor Gray
            Write-Host "  • notebooklm : Nghiên cứu tài liệu sâu qua Google NotebookLM" -ForegroundColor Gray
            Write-Host "  • knowledge  : Context cache, memory consolidation (đi kèm Second Brain)" -ForegroundColor Gray
            Write-Host "  • maintainer : Bộ công cụ nội bộ bảo trì kit (validate-kit.ps1)" -ForegroundColor Gray
            Write-Host ""
            Write-Host "👉 Để xem chi tiết và cài addon, gõ: adk addon (hoặc adk addon add <tên>)" -ForegroundColor Cyan
            Write-Host ""
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
                param(
                    [string]$cmd = "init",
                    [string]$subcmd = "",
                    [switch]$Force
                )
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
                    { $_ -in "addon", "addons" } {
                        if ($runLocal -and (Test-Path "$localKit\addon.ps1")) {
                            & "$localKit\addon.ps1" $subcmd $args
                        } elseif (Test-Path ".agents\addon.ps1") {
                            & ".\.agents\addon.ps1" $subcmd $args
                        } else {
                            irm "$remoteRepo/addon.ps1" | iex
                        }
                    }
                    { $_ -in "v", "ver", "version", "-v", "--version" } {
                        $ver = "unknown"
                        if (Test-Path ".agents\VERSION") { $ver = (Get-Content ".agents\VERSION" -Raw).Trim() }
                        elseif ($runLocal -and (Test-Path "$localKit\VERSION")) { $ver = (Get-Content "$localKit\VERSION" -Raw).Trim() }
                        Write-Host "🤖 Agent-Dev-Kit v$ver" -ForegroundColor Cyan
                    }
                    { $_ -in "help", "-h", "--help" } {
                        Write-Host ""
                        Write-Host "========================================================================" -ForegroundColor Cyan
                        Write-Host "   🤖 AGENT-DEV-KIT CLI (adk) — Hướng Dẫn Sử Dụng                       " -ForegroundColor Cyan
                        Write-Host "========================================================================" -ForegroundColor Cyan
                        Write-Host ""
                        Write-Host "📌 1. LỆNH CLI CƠ BẢN:" -ForegroundColor Yellow
                        Write-Host "  adk, adk i, adk install   : Khởi tạo kit vào project (.agents/)" -ForegroundColor White
                        Write-Host "  adk up, adk update        : Cập nhật core kit lên bản mới nhất" -ForegroundColor White
                        Write-Host "  adk addon [tên]           : Quản lý, xem link và cài đặt addons" -ForegroundColor White
                        Write-Host "  adk version, adk -v       : Xem phiên bản hiện tại" -ForegroundColor White
                        Write-Host "  adk help, adk --help      : Xem bảng trợ giúp này" -ForegroundColor White
                        Write-Host ""
                        Write-Host "💬 2. CÁCH DÙNG TRONG CHAT (WORKFLOWS):" -ForegroundColor Yellow
                        Write-Host "  /wf-scout                 : Khảo sát, đọc hiểu codebase dự án" -ForegroundColor White
                        Write-Host "  /wf-plan <tính năng>     : Lên kế hoạch chi tiết trước khi code" -ForegroundColor White
                        Write-Host "  /wf-cook                  : Triển khai code bám sát plan đã duyệt" -ForegroundColor White
                        Write-Host "  /wf-fix <lỗi>             : Chẩn đoán và sửa lỗi theo quy trình" -ForegroundColor White
                        Write-Host "  /wf-test                  : Sinh unit test và kịch bản kiểm thử" -ForegroundColor White
                        Write-Host "  /wf-review                : Rà soát chất lượng code và regression" -ForegroundColor White
                        Write-Host ""
                        Write-Host "📦 3. DANH SÁCH 6 ADDONS (Gõ 'adk addon' để chọn và cài đặt):" -ForegroundColor Yellow
                        Write-Host "  • archify    : Vẽ sơ đồ HTML tương tác (https://vividkit.dev/vi/guides/archify)" -ForegroundColor Gray
                        Write-Host "  • database   : Tra cứu schema & query an toàn qua Gridex MCP" -ForegroundColor Gray
                        Write-Host "  • obsidian   : Đồng bộ tri thức hai chiều với Second Brain (https://obsidian.md)" -ForegroundColor Gray
                        Write-Host "  • notebooklm : Nghiên cứu tài liệu sâu qua Google NotebookLM" -ForegroundColor Gray
                        Write-Host "  • knowledge  : Context cache, memory consolidation (đi kèm Second Brain)" -ForegroundColor Gray
                        Write-Host "  • maintainer : Bộ công cụ nội bộ bảo trì kit (validate-kit.ps1)" -ForegroundColor Gray
                        Write-Host ""
                        Write-Host "👉 Để xem chi tiết và cài addon, gõ: adk addon (hoặc adk addon add <tên>)" -ForegroundColor Cyan
                        Write-Host ""
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
    Write-Host "🚀 Sẵn sàng! Bạn có thể bắt đầu chat ngay với AI mà không cần cấu hình gì thêm." -ForegroundColor Cyan
    Write-Host "💡 Gợi ý: Gõ 'adk up' bất cứ khi nào muốn cập nhật kit lên bản mới nhất." -ForegroundColor DarkGray
}
finally {
    if (Test-Path $TempDir) {
        Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
