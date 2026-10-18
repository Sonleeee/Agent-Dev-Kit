<#
.SYNOPSIS
    Agent-Dev-Kit Installer (adk init)
.DESCRIPTION
    Khởi tạo Agent-Dev-Kit vào project hiện tại.
    Tự động chuẩn bị .agents/, AGENTS.md và bảo vệ context dự án.
#>
[CmdletBinding()]
param(
    [switch]$Force,
    [switch]$Full
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
    # 1. Tìm nguồn kit (ưu tiên: chính thư mục .agents/ đã clone > local dev > GitHub)
    if (Test-Path (Join-Path $PSScriptRoot "templates\AGENTS.md.template")) {
        $SourcePath = $PSScriptRoot
    } elseif (Test-Path $LocalKitPath) {
        Write-Host "📦 Sử dụng nguồn Agent-Dev-Kit cục bộ: $LocalKitPath" -ForegroundColor Gray
        $SourcePath = $LocalKitPath
    } else {
        Write-Host "🌐 Đang tải Agent-Dev-Kit mới nhất từ GitHub ($RepoUrl)..." -ForegroundColor Gray
        git clone --depth 1 $RepoUrl $TempDir --quiet 2>$null
        if (-not (Test-Path $TempDir) -or (Get-ChildItem $TempDir -ErrorAction SilentlyContinue).Count -eq 0) {
            git clone --depth 1 "git@github.com:Sonleeee/Agent-Dev-Kit.git" $TempDir --quiet 2>$null
        }
        $SourcePath = $TempDir
    }

    # 2. Tạo thư mục .agents nếu chưa có
    if (-not (Test-Path $TargetAgentsDir)) {
        New-Item -ItemType Directory -Path $TargetAgentsDir -Force | Out-Null
        Write-Host "📁 Đã tạo thư mục .agents/" -ForegroundColor Green
    }

    # 3. Copy các thành phần Core (bỏ qua nếu đã clone trực tiếp vào .agents)
    $CoreItems = @(
        "workflows", "skills", "rules", "agents", "templates",
        "schemas", "addons", "tools",
        "SYSTEM.md", "README.md", "CHANGELOG.md", "VERSION", "addon.ps1"
    )

    $isAlreadyInTarget = $false
    if (Test-Path $TargetAgentsDir) {
        $srcFull = (Get-Item $SourcePath).FullName
        $tgtFull = (Get-Item $TargetAgentsDir).FullName
        if ($srcFull -eq $tgtFull) {
            $isAlreadyInTarget = $true
        }
    }

    if (-not $isAlreadyInTarget) {
        Write-Host "🚀 Đang sao chép các thành phần Core..." -ForegroundColor Gray
        # Dọn dẹp các thư mục rác cũ đã khai tử của Kit (không xóa file riêng của user)
        $ObsoleteItems = @("quality", "registry", "docs", "context")
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
    } else {
        Write-Host "📦 Core Kit đã sẵn sàng trong .agents/" -ForegroundColor Gray
    }

    # 4. Tạo AGENTS.md tại root (nếu chưa có)
    $AgentsFile = Join-Path $CurrentDir "AGENTS.md"
    if (-not (Test-Path $AgentsFile)) {
        $TemplateAgents = Join-Path $SourcePath "templates\AGENTS.md.template"
        if (Test-Path $TemplateAgents) {
            Copy-Item -Path $TemplateAgents -Destination $AgentsFile -Force
            Write-Host "📄 Đã tạo AGENTS.md tại thư mục gốc" -ForegroundColor Green
        }
    } else {
        Write-Host "ℹ️  AGENTS.md đã có sẵn, giữ nguyên an toàn." -ForegroundColor Yellow
        # Gợi ý user nhờ AI thêm section kit nếu chưa có
        $agentsContent = Get-Content $AgentsFile -Raw -ErrorAction SilentlyContinue
        if ($agentsContent -notmatch "Agent-Dev-Kit") {
            Write-Host "💡 Gợi ý: Gõ cho AI: " -ForegroundColor Cyan -NoNewline
            Write-Host '"Đọc .agents/templates/AGENTS.md.template rồi thêm section Agent-Dev-Kit vào AGENTS.md"' -ForegroundColor White
        }
    }

    # 5. Kiểm tra tùy chọn CodeGraph
    $setupCodeGraph = $Full.IsPresent
    if (-not $Full -and -not $Force) {
        try {
            Write-Host ""
            $cgAns = Read-Host "👉 Bạn có muốn cài đặt & lập chỉ mục CodeGraph (AST & Call Graph) luôn không? [Y/n] (Mặc định: Y)"
            if ([string]::IsNullOrWhiteSpace($cgAns) -or $cgAns -match "^[yY]") {
                $setupCodeGraph = $true
            }
        } catch {
            # Bỏ qua nếu chạy non-interactive
        }
    }

    # 6. Thêm .agents và .codegraph vào .gitignore nếu có git
    $GitIgnoreFile = Join-Path $CurrentDir ".gitignore"
    if (Test-Path $GitIgnoreFile) {
        $giContent = Get-Content $GitIgnoreFile -Raw -ErrorAction SilentlyContinue
        if ($giContent -notmatch "(?m)^\.agents/?$") {
            Add-Content -Path $GitIgnoreFile -Value "`n.agents/"
            Write-Host "🔒 Đã thêm .agents/ vào .gitignore" -ForegroundColor Green
        }
        if ($setupCodeGraph -and ($giContent -notmatch "(?m)^\.codegraph/?$")) {
            Add-Content -Path $GitIgnoreFile -Value ".codegraph/"
            Write-Host "🔒 Đã thêm .codegraph/ vào .gitignore" -ForegroundColor Green
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

            $adkSnippet = @'
# --- AGENT-DEV-KIT-CLI-START ---
function global:adk {
    param(
        [string]$cmd = "help",
        [string]$subcmd = "",
        [switch]$Force,
        [switch]$Full
    )
    $localKit = "C:\Sonlee\AI\Agent-Dev-Kit"
    $remoteRepo = "https://raw.githubusercontent.com/Sonleeee/Agent-Dev-Kit/main"
    $runLocal = Test-Path $localKit

    switch ($cmd.ToLower()) {
        { $_ -in "i", "init", "install" } {
            $isFull = $Full.IsPresent -or ($subcmd -in "full", "--full", "-full", "all")
            if ($runLocal) { & "$localKit\install.ps1" -Force:$Force -Full:$isFull }
            else { & ([scriptblock]::Create((irm "$remoteRepo/install.ps1"))) -Force:$Force -Full:$isFull }
        }
        { $_ -in "full", "setup", "all" } {
            if ($runLocal) { & "$localKit\install.ps1" -Force:$Force -Full }
            else { & ([scriptblock]::Create((irm "$remoteRepo/install.ps1"))) -Force:$Force -Full }
        }
        { $_ -in "u", "up", "update" } {
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
        { $_ -in "profile" } {
            if ($runLocal -and (Test-Path "$localKit\tools\init-profile.ps1")) {
                & "$localKit\tools\init-profile.ps1"
            } elseif (Test-Path ".agents\tools\init-profile.ps1") {
                & ".\.agents\tools\init-profile.ps1"
            } else {
                irm "$remoteRepo/tools/init-profile.ps1" | iex
            }
        }
        { $_ -in "v", "ver", "version", "-v", "--version" } {
            $ver = "unknown"
            if (Test-Path ".agents\VERSION") { $ver = (Get-Content ".agents\VERSION" -Raw).Trim() }
            elseif ($runLocal -and (Test-Path "$localKit\VERSION")) { $ver = (Get-Content "$localKit\VERSION" -Raw).Trim() }
            Write-Host "🤖 Agent-Dev-Kit v$ver" -ForegroundColor Cyan
        }
        { $_ -in "help", "-h", "--help", "" } {
            Write-Host ""
            Write-Host "========================================================================" -ForegroundColor Cyan
            Write-Host "   🤖 AGENT-DEV-KIT CLI (adk) — Hướng Dẫn Sử Dụng                       " -ForegroundColor Cyan
            Write-Host "========================================================================" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "📌 1. LỆNH CLI CƠ BẢN:" -ForegroundColor Yellow
            Write-Host "  adk, adk help, adk -h     : Hiển thị bảng trợ giúp này" -ForegroundColor White
            Write-Host "  adk i, adk install        : Tải/Khởi tạo kit vào project (.agents/)" -ForegroundColor White
            Write-Host "  adk full, adk setup       : Full Setup 1-chạm (.agents/ + AGENTS.md + CodeGraph MCP & Index)" -ForegroundColor White
            Write-Host "  adk u, adk update         : Cập nhật core kit lên bản mới nhất" -ForegroundColor White
            Write-Host "  adk profile               : Thiết lập gu code cá nhân (~/.agents/developer.md)" -ForegroundColor White
            Write-Host "  adk addon [tên]           : Quản lý và cài đặt addons (codegraph, archify...)" -ForegroundColor White
            Write-Host "  adk version, adk -v       : Xem phiên bản hiện tại" -ForegroundColor White
            Write-Host ""
            Write-Host "💬 2. QUY TRÌNH CHUẨN TRONG CHAT (WORKFLOWS):" -ForegroundColor Yellow
            Write-Host "  /wf-clarify <yêu cầu>    : Làm rõ yêu cầu & chốt Invariants" -ForegroundColor White
            Write-Host "  /wf-plan <tính năng>     : Lập kế hoạch & sinh Execution Contract" -ForegroundColor White
            Write-Host "  /wf-impl                  : Triển khai code bám sát Contract" -ForegroundColor White
            Write-Host "  /wf-review                : Rà soát 4 tầng & kiểm tra Executable Gates" -ForegroundColor White
            Write-Host "  /wf-fix <lỗi>             : Chẩn đoán nguyên nhân gốc & sửa lỗi" -ForegroundColor White
            Write-Host "  /wf-evolve                : Tự động phân tích logs & tối ưu hóa rules" -ForegroundColor White
            Write-Host ""
            Write-Host "📦 3. DANH SÁCH 5 ADDONS (Gõ 'adk addon' để chọn và cài đặt):" -ForegroundColor Yellow
            Write-Host "  • codegraph  : Lập chỉ mục AST, call graph & symbols (giảm 35% token)" -ForegroundColor Gray
            Write-Host "  • archify    : Vẽ sơ đồ HTML tương tác (https://vividkit.dev/vi/guides/archify)" -ForegroundColor Gray
            Write-Host "  • database   : Tra cứu schema & query an toàn qua Gridex MCP" -ForegroundColor Gray
            Write-Host "  • obsidian   : Đồng bộ tri thức hai chiều với Second Brain (https://obsidian.md)" -ForegroundColor Gray
            Write-Host "  • notebooklm : Nghiên cứu tài liệu sâu qua Google NotebookLM" -ForegroundColor Gray
            Write-Host ""
            Write-Host "👉 Để xem chi tiết và cài addon, gõ: adk addon (hoặc adk addon add <tên>)" -ForegroundColor Cyan
            Write-Host ""
        }
        default {
            Write-Warning "Lệnh không hợp lệ: '$cmd'. Gõ 'adk' hoặc 'adk help' để xem hướng dẫn."
        }
    }
}
# --- AGENT-DEV-KIT-CLI-END ---
'@

            $profileContent = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue
            if ($profileContent -match "(?s)# --- (AGENT-DEV-KIT-CLI-START|Agent-Dev-Kit CLI \(adk\)) ---.*# --- AGENT-DEV-KIT-CLI-END ---") {
                $newProfile = [regex]::Replace($profileContent, "(?s)# --- (AGENT-DEV-KIT-CLI-START|Agent-Dev-Kit CLI \(adk\)) ---.*# --- AGENT-DEV-KIT-CLI-END ---", $adkSnippet.Trim())
                [System.IO.File]::WriteAllText($PROFILE, $newProfile, [System.Text.Encoding]::UTF8)
                Write-Host "⚡ Đã cập nhật lệnh 'adk' trong PowerShell Profile!" -ForegroundColor Green
            } elseif ($profileContent -notmatch "function\s+global:adk\b") {
                [System.IO.File]::AppendAllText($PROFILE, "`n$adkSnippet`n", [System.Text.Encoding]::UTF8)
                Write-Host "⚡ Đã tự động đăng ký lệnh 'adk' vào PowerShell Profile!" -ForegroundColor Green
            }

            # Nạp ngay function adk vào phiên hiện tại để dùng được luôn
            Invoke-Expression $adkSnippet
        }
    } catch {
        Write-Verbose "Không thể tự động cập nhật profile: $_"
    }

    # 7. Cài đặt và lập chỉ mục CodeGraph (nếu chọn)
    if ($setupCodeGraph) {
        Write-Host ""
        Write-Host "🔍 [CodeGraph] Đang tự động kết nối MCP Server và lập chỉ mục mã nguồn..." -ForegroundColor Cyan
        try {
            if ($IsWindows -or ($env:OS -eq "Windows_NT")) {
                cmd.exe /c "npx -y @colbymchenry/codegraph install -y -i --target=antigravity,codex"
            } else {
                npx -y @colbymchenry/codegraph install -y -i --target=antigravity,codex
            }
            Write-Host "✅ [CodeGraph] Đã cài đặt MCP & hoàn tất chỉ mục AST/Call Graph cho dự án!" -ForegroundColor Green
        } catch {
            Write-Warning "Không thể tự động kích hoạt CodeGraph: $_. Bạn có thể thử lại sau bằng lệnh: adk addon codegraph"
        }
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