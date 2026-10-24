<#
.SYNOPSIS
    Agent-Dev-Kit Addon Manager (adk addon)
.DESCRIPTION
    Quản lý, hiển thị link cài đặt và kích hoạt các addons có tương tác với người dùng.
#>
[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [string]$Action = "list",

    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Name = @()
)

$NameStr = ($Name -join " ").Trim()

$LocalKitPath = if ($env:ADK_HOME -and (Test-Path $env:ADK_HOME)) { $env:ADK_HOME } elseif (Test-Path (Join-Path $PSScriptRoot "addons")) { $PSScriptRoot } else { Join-Path (Get-Location) ".agents" }
if (-not (Test-Path $LocalKitPath)) {
    $LocalKitPath = Join-Path (Get-Location) ".agents"
}

# Danh mục 7 Addons chính thức
$AddonsData = @{
    "ui-design" = @{
        Title       = "UI Design (Craftsmanship and Anti-Slop MCP)"
        Description = "Kho Design Tokens, 8 Archetypes, Emil Kowalski Motion Physics, 20-Rule Quality Gate va scaffold DESIGN.md qua MCP."
        DocsUrl     = "https://github.com/Sonleeee/Agent-Dev-Kit/tree/main/addons/ui-design"
        RepoUrl     = ""
        InstallCmd  = "powershell -File .agents/addons/ui-design/setup.ps1"
        Type        = "MCP Server / CLI"
    }
    "system-design" = @{
        Title       = "System Design (Knowledge Base & Scaffolding MCP)"
        Description = "Kho kiến trúc tham khảo (Outbox, Idempotency, Circuit Breaker...) và skill scaffold source base theo yêu cầu qua MCP."
        DocsUrl     = "https://github.com/Sonleeee/Agent-Dev-Kit/tree/main/addons/system-design"
        RepoUrl     = ""
        InstallCmd  = "powershell -File .agents/addons/system-design/setup.ps1"
        Type        = "MCP Server / CLI"
    }
    "codegraph" = @{
        Title       = "CodeGraph (Semantic Code Intelligence)"
        Description = "Lap chi muc AST, call graph, symbol relationships (19+ ngon ngu). Giam ~35% token va ~70% tool calls."
        DocsUrl     = "https://github.com/colbymchenry/codegraph"
        RepoUrl     = "https://github.com/colbymchenry/codegraph"
        InstallCmd  = "npx -y @colbymchenry/codegraph install -y --target=antigravity,codex"
        Type        = "MCP Server / CLI"
    }
    "database" = @{
        Title       = "Database Inspector (Gridex MCP)"
        Description = "Tra cứu cấu trúc bảng (schema), quan hệ khóa ngoại và thực thi SQL chỉ đọc an toàn để debug LINQ/EF Core."
        DocsUrl     = "https://github.com/Sonleeee/Agent-Dev-Kit/tree/main/addons/database"
        RepoUrl     = ""
        InstallCmd  = ""
        Type        = "MCP Server (Gridex)"
    }
    "obsidian" = @{
        Title       = "Obsidian (Second Brain Integration)"
        Description = "Đọc và lưu tri thức, ADR hoặc bài học vào Obsidian Vault theo yêu cầu rõ ràng."
        DocsUrl     = "https://obsidian.md"
        RepoUrl     = "https://obsidian.md/download"
        InstallCmd  = ""
        Type        = "App & Vault"
    }
    "notebooklm" = @{
        Title       = "NotebookLM (Research & Task Sync)"
        Description = "Nghiên cứu tài liệu kỹ thuật chuyên sâu, tổng hợp tri thức và đồng bộ ghi chú từ thiết bị di động."
        DocsUrl     = "https://notebooklm.google.com"
        RepoUrl     = ""
        InstallCmd  = ""
        Type        = "MCP Server (NotebookLM)"
    }
    "maintainer" = @{
        Title       = "Maintainer Tools (Health Check & Skill Creator)"
        Description = "Bộ công cụ nội bộ kiểm tra tính toàn vẹn (validate-kit.ps1) và sinh skill mới chuẩn spec cho kit."
        DocsUrl     = "https://github.com/Sonleeee/Agent-Dev-Kit/tree/main/addons/maintainer"
        RepoUrl     = ""
        InstallCmd  = "powershell -File .agents/tools/validate-kit.ps1"
        Type        = "Kit Script"
    }
}

function Export-AddonSkills([string]$AddonKey) {
    $sourceRoot = Join-Path $LocalKitPath "addons\$AddonKey"
    if (-not (Test-Path $sourceRoot)) { return }

    $targetRoot = Join-Path (Get-Location) ".agents\skills"
    New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null
    $skillDirs = Get-ChildItem -Path $sourceRoot -Directory -Recurse |
        Where-Object { ($_.Name -like "adk-*" -or $_.Name -like "sk-*") -and (Test-Path (Join-Path $_.FullName "SKILL.md")) } |
        Sort-Object FullName
    $seen = @{}
    $exported = 0

    foreach ($skillDir in $skillDirs) {
        $skillName = $skillDir.Name
        if ($seen.ContainsKey($skillName)) { continue }
        $seen[$skillName] = $true

        $destination = Join-Path $targetRoot $skillName
        $marker = Join-Path $destination ".adk-managed"
        if ((Test-Path $destination) -and -not (Test-Path $marker)) {
            Write-Warning "Giữ nguyên skill người dùng '$skillName'; không ghi đè."
            continue
        }

        New-Item -ItemType Directory -Path $destination -Force | Out-Null
        Get-ChildItem -Path $skillDir.FullName -Force |
            ForEach-Object { Copy-Item -Path $_.FullName -Destination $destination -Recurse -Force }
        New-Item -ItemType File -Path $marker -Force | Out-Null
        $exported++
    }

    if ($exported -gt 0) {
        Write-Host "🧩 Đã export $exported skill của addon '$AddonKey' vào .agents/skills/." -ForegroundColor Gray
    }
}

function Show-Addon-Details([string]$key) {
    if (-not $AddonsData.ContainsKey($key)) {
        Write-Warning "Không tìm thấy addon '$key'. Hãy gõ 'adk addon list' để xem danh sách."
        return
    }

    $addon = $AddonsData[$key]
    Write-Host ""
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host "  📦 ADDON: $($addon.Title)" -ForegroundColor Cyan
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host "📝 Mô tả     : $($addon.Description)" -ForegroundColor Gray
    Write-Host "🏷️  Loại      : $($addon.Type)" -ForegroundColor DarkGray
    if ($addon.DocsUrl) {
        Write-Host "🔗 Tài liệu  : $($addon.DocsUrl)" -ForegroundColor Yellow
    }
    if ($addon.RepoUrl) {
        Write-Host "🔗 Trang tải : $($addon.RepoUrl)" -ForegroundColor Yellow
    }
    Write-Host "------------------------------------------------------------------------" -ForegroundColor DarkGray

    # Menu tương tác cho từng loại addon
    switch ($key) {
        "ui-design" {
            Write-Host "LỰA CHỌN CỦA BẠN:" -ForegroundColor Cyan
            Write-Host "  [1] Tự động cài đặt và cấu hình UI Design MCP Server (Antigravity & Claude)" -ForegroundColor White
            Write-Host "  [2] Thử nghiệm lệnh tra cứu Archetype (node addons/ui-design/mcp-server/index.js search)" -ForegroundColor White
            Write-Host "  [0] Quay lại / Hủy" -ForegroundColor DarkGray
            $opt = Read-Host "👉 Nhập lựa chọn của bạn [0-2] (Mặc định: 1)"
            if ([string]::IsNullOrWhiteSpace($opt)) { $opt = "1" }

            switch ($opt) {
                "1" {
                    $setupScript = Join-Path $LocalKitPath "addons\ui-design\setup.ps1"
                    if (Test-Path $setupScript) {
                        & $setupScript
                    } else {
                        node (Join-Path $LocalKitPath "addons\ui-design\setup.js")
                    }
                }
                "2" {
                    node (Join-Path $LocalKitPath "addons\ui-design\mcp-server\index.js") search
                }
                default { Write-Host "Đã hủy thao tác." -ForegroundColor DarkGray }
            }
        }
        "system-design" {
            Write-Host "LỰA CHỌN CỦA BẠN:" -ForegroundColor Cyan
            Write-Host "  [1] Tự động cài đặt và cấu hình System Design MCP Server (Antigravity & Claude)" -ForegroundColor White
            Write-Host "  [2] Xem danh sách kiến trúc mẫu (blueprints)" -ForegroundColor White
            Write-Host "  [0] Quay lại / Hủy" -ForegroundColor DarkGray
            $opt = Read-Host "👉 Nhập lựa chọn của bạn [0-2] (Mặc định: 1)"
            if ([string]::IsNullOrWhiteSpace($opt)) { $opt = "1" }

            switch ($opt) {
                "1" {
                    $setupScript = Join-Path $LocalKitPath "addons\system-design\setup.ps1"
                    if (Test-Path $setupScript) {
                        & $setupScript
                    } else {
                        node (Join-Path $LocalKitPath "addons\system-design\setup.js")
                    }
                }
                "2" {
                    node (Join-Path $LocalKitPath "addons\system-design\mcp-server\index.js") blueprints
                }
                default { Write-Host "Đã hủy thao tác." -ForegroundColor DarkGray }
            }
        }
        "codegraph" {
            Write-Host "LUA CHON CUA BAN:" -ForegroundColor Cyan
            Write-Host "  [1] Tu dong cai dat CodeGraph MCP Server (Antigravity & Codex)" -ForegroundColor White
            Write-Host "  [2] Khoi tao chi muc CodeGraph cho du an hien tai (codegraph init -i)" -ForegroundColor White
            Write-Host "  [3] Mo trang GitHub repo cua CodeGraph" -ForegroundColor White
            Write-Host "  [0] Quay lai / Huy" -ForegroundColor DarkGray
            $opt = Read-Host "Nhap lua chon cua ban [0-3] (Mac dinh: 1)"
            if ([string]::IsNullOrWhiteSpace($opt)) { $opt = "1" }

            switch ($opt) {
                "1" {
                    Write-Host "Dang cai dat CodeGraph MCP Server cho Antigravity & Codex..." -ForegroundColor Cyan
                    if ($IsWindows -or ($env:OS -eq "Windows_NT")) {
                        cmd.exe /c "npx -y @colbymchenry/codegraph install -y --target=antigravity,codex"
                    } else {
                        npx -y @colbymchenry/codegraph install -y --target=antigravity,codex
                    }
                    Write-Host "Hoan tat cau hinh CodeGraph MCP Server!" -ForegroundColor Green
                }
                "2" {
                    Write-Host "Dang khoi tao chi muc CodeGraph: codegraph init -i..." -ForegroundColor Cyan
                    codegraph init -i
                }
                "3" { Start-Process $addon.RepoUrl }
                default { Write-Host "Da huy thao tac." -ForegroundColor DarkGray }
            }
        }
        "database" {
            Write-Host "LỰA CHỌN CỦA BẠN:" -ForegroundColor Cyan
            Write-Host "  [1] Kiểm tra xem hệ thống đã có Gridex MCP Server chưa" -ForegroundColor White
            Write-Host "  [2] Xem hướng dẫn sử dụng Gridex trong skill adk-db-inspector" -ForegroundColor White
            Write-Host "  [0] Quay lại / Hủy" -ForegroundColor DarkGray
            $opt = Read-Host "👉 Nhập lựa chọn của bạn [0-2] (Mặc định: 1)"
            if ([string]::IsNullOrWhiteSpace($opt)) { $opt = "1" }

            switch ($opt) {
                "1" {
                    Write-Host "🔍 Đang kiểm tra cấu hình Gridex MCP..." -ForegroundColor Cyan
                    # Kiểm tra config mcp
                    $mcpFound = $false
                    $possibleConfigs = @(
                        "$env:USERPROFILE\.gemini\antigravity\mcp\gridex",
                        "$env:USERPROFILE\.cursor\mcp.json",
                        "$env:APPDATA\Claude\claude_desktop_config.json"
                    )
                    foreach ($cfg in $possibleConfigs) {
                        if (Test-Path $cfg) { $mcpFound = $true; break }
                    }
                    if ($mcpFound) {
                        Write-Host "✅ Đã tìm thấy Gridex MCP trên máy của bạn!" -ForegroundColor Green
                        Write-Host "💡 Khi chat, AI có thể tự gọi các tool: list_tables, describe_table, query (readonly)..." -ForegroundColor Yellow
                    } else {
                        Write-Host "ℹ️  Chưa phát hiện Gridex MCP. Hãy đảm bảo bạn đã thêm server Gridex vào cấu hình MCP." -ForegroundColor Yellow
                    }
                }
                "2" {
                    $skillFile = Join-Path $LocalKitPath "addons\database\skills\adk-db-inspector\SKILL.md"
                    if (Test-Path $skillFile) {
                        Get-Content $skillFile | Select-Object -First 35
                    } else {
                        Write-Host "Xem tại: https://github.com/Sonleeee/Agent-Dev-Kit/tree/main/addons/database" -ForegroundColor Yellow
                    }
                }
                default { Write-Host "Đã hủy thao tác." -ForegroundColor DarkGray }
            }
        }
        "obsidian" {
            Write-Host "LỰA CHỌN CỦA BẠN:" -ForegroundColor Cyan
            Write-Host "  [1] Cấu hình đường dẫn Obsidian Vault (vault-path) vào AGENTS.md" -ForegroundColor White
            Write-Host "  [2] Mở trang chủ / Tải Obsidian (https://obsidian.md)" -ForegroundColor White
            Write-Host "  [0] Quay lại / Hủy" -ForegroundColor DarkGray
            $opt = Read-Host "👉 Nhập lựa chọn của bạn [0-2] (Mặc định: 1)"
            if ([string]::IsNullOrWhiteSpace($opt)) { $opt = "1" }

            switch ($opt) {
                "1" {
                    $vaultInput = Read-Host "👉 Nhập đường dẫn thư mục Obsidian Vault của bạn"
                    if ([string]::IsNullOrWhiteSpace($vaultInput)) {
                        Write-Warning "Bạn chưa nhập đường dẫn vault. Hủy thao tác."
                        return
                    }

                    if (Test-Path ".\AGENTS.md") {
                        $content = Get-Content ".\AGENTS.md" -Raw
                        if ($content -match "vault-path:") {
                            $content = $content -replace "vault-path:.*", "vault-path: $vaultInput"
                            [System.IO.File]::WriteAllText(".\AGENTS.md", $content, [System.Text.Encoding]::UTF8)
                            Write-Host "✅ Đã cập nhật vault-path thành: $vaultInput trong AGENTS.md!" -ForegroundColor Green
                        } else {
                            Add-Content ".\AGENTS.md" "`n- **vault-path:** $vaultInput" -Encoding utf8
                            Write-Host "✅ Đã thêm vault-path: $vaultInput vào AGENTS.md!" -ForegroundColor Green
                        }
                    } else {
                        Write-Warning "Không tìm thấy file AGENTS.md tại thư mục hiện tại. Hãy chạy 'adk i' trước."
                    }
                }
                "2" { Start-Process "https://obsidian.md/download" }
                default { Write-Host "Đã hủy thao tác." -ForegroundColor DarkGray }
            }
        }
        "notebooklm" {
            Write-Host "LỰA CHỌN CỦA BẠN:" -ForegroundColor Cyan
            Write-Host "  [1] Kiểm tra kết nối NotebookLM MCP Server trên máy" -ForegroundColor White
            Write-Host "  [2] Mở trang web Google NotebookLM (https://notebooklm.google.com)" -ForegroundColor White
            Write-Host "  [0] Quay lại / Hủy" -ForegroundColor DarkGray
            $opt = Read-Host "👉 Nhập lựa chọn của bạn [0-2] (Mặc định: 1)"
            if ([string]::IsNullOrWhiteSpace($opt)) { $opt = "1" }

            switch ($opt) {
                "1" {
                    $mcpPath = "$env:USERPROFILE\.gemini\antigravity\mcp\notebooklm"
                    if (Test-Path $mcpPath) {
                        Write-Host "✅ Đã tìm thấy NotebookLM MCP Server trên máy của bạn!" -ForegroundColor Green
                        Write-Host "💡 AI có thể dùng notebook_query, notebook_list để nghiên cứu tài liệu tự động." -ForegroundColor Yellow
                    } else {
                        Write-Host "ℹ️  Hãy đảm bảo NotebookLM MCP Server đã được cấu hình trong MCP settings." -ForegroundColor Yellow
                    }
                }
                "2" { Start-Process "https://notebooklm.google.com" }
                default { Write-Host "Đã hủy thao tác." -ForegroundColor DarkGray }
            }
        }
        "maintainer" {
            Write-Host "LỰA CHỌN CỦA BẠN:" -ForegroundColor Cyan
            Write-Host "  [1] Chạy kiểm tra toàn diện kit ngay bây giờ (validate-kit.ps1)" -ForegroundColor White
            Write-Host "  [2] Xem hướng dẫn tạo skill mới" -ForegroundColor White
            Write-Host "  [0] Quay lại / Hủy" -ForegroundColor DarkGray
            $opt = Read-Host "👉 Nhập lựa chọn của bạn [0-2] (Mặc định: 1)"
            if ([string]::IsNullOrWhiteSpace($opt)) { $opt = "1" }

            switch ($opt) {
                "1" {
                    $valScript = Join-Path $LocalKitPath "tools\validate-kit.ps1"
                    if (Test-Path $valScript) {
                        & $valScript
                    } else {
                        Write-Warning "Không tìm thấy $valScript"
                    }
                }
                "2" {
                    $creatorSkill = Join-Path $LocalKitPath "addons\maintainer\skills\adk-skill-creator\SKILL.md"
                    if (Test-Path $creatorSkill) {
                        Get-Content $creatorSkill | Select-Object -First 30
                    }
                }
                default { Write-Host "Đã hủy thao tác." -ForegroundColor DarkGray }
            }
        }
    }
}

# Xử lý các Action
$target = if ($NameStr) { $NameStr.ToLower() } else { $Action.ToLower() }

if ($target -in "list", "ls", "all", "") {
    Write-Host ""
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host "   📦 AGENT-DEV-KIT ADDONS (6 Addons khả dụng)                          " -ForegroundColor Cyan
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host ""
    $i = 1
    $keys = @("ui-design", "system-design", "codegraph", "database", "obsidian", "notebooklm")
    foreach ($k in $keys) {
        $item = $AddonsData[$k]
        Write-Host "  $i. $($k.PadRight(12)) : $($item.Title)" -ForegroundColor White
        Write-Host "     📝 $($item.Description)" -ForegroundColor Gray
        if ($item.DocsUrl) {
            Write-Host "     🔗 Link: $($item.DocsUrl)" -ForegroundColor DarkCyan
        }
        Write-Host ""
        $i++
    }
    Write-Host "------------------------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host "👉 Cú pháp: adk addon add <tên-addon> để xem tùy chọn và cài đặt." -ForegroundColor Yellow
    Write-Host "   Ví dụ  : adk addon add codegraph" -ForegroundColor DarkGray
    Write-Host ""
    $choice = Read-Host "Nhập tên hoặc số thứ tự addon bạn muốn xem/cài đặt [1-6 / Enter để thoát]"
    if ($choice -match '^[1-6]$') {
        $selectedKey = $keys[[int]$choice - 1]
        Show-Addon-Details $selectedKey
    } elseif ($AddonsData.ContainsKey($choice.ToLower())) {
        Show-Addon-Details $choice.ToLower()
    }
}
elseif ($Action.ToLower() -in "add", "install", "i") {
    if ($NameStr -and $AddonsData.ContainsKey($NameStr.ToLower())) {
        Export-AddonSkills $NameStr.ToLower()
        Show-Addon-Details $NameStr.ToLower()
    } else {
        $inputName = Read-Host "👉 Nhập tên addon bạn muốn thêm (codegraph, system-design, database, obsidian, notebooklm)"
        if ($AddonsData.ContainsKey($inputName.ToLower())) {
            Export-AddonSkills $inputName.ToLower()
            Show-Addon-Details $inputName.ToLower()
        } else {
            Write-Warning "Không tìm thấy addon '$inputName'. Hãy chạy 'adk addon' để xem danh sách."
        }
    }
}
elseif ($AddonsData.ContainsKey($target)) {
    Show-Addon-Details $target
}
else {
    Write-Warning "Lệnh không hợp lệ: '$Action'. Dùng 'adk addon' hoặc 'adk addon add <tên-addon>'."
}
