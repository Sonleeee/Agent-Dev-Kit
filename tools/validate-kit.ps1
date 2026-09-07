param(
    [string]$KitRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
$failures = [System.Collections.Generic.List[string]]::new()

function Require-Path([string]$RelativePath) {
    if (-not (Test-Path (Join-Path $KitRoot $RelativePath))) {
        $failures.Add("Missing: $RelativePath")
    }
}

@(
    'AGENTS.md', 'SYSTEM.md', 'README.md', 'rules/global.md',
    'templates/execution-contract.md.template',
    'skills/core/sk-execution-contract/SKILL.md',
    '_project-template/AGENTS.md',
    '_project-template/.agents/context/manifest.md.template'
) | ForEach-Object { Require-Path $_ }

$workflowDocs = Get-ChildItem -Path $KitRoot -Recurse -File -Filter '*.md' |
    Where-Object { $_.Name -ne 'CHANGELOG.md' -and $_.FullName -notmatch '\\to-do\\' }

$workflowRefs = $workflowDocs |
    Select-String -Pattern '/wf-[a-z0-9-]+' -AllMatches |
    ForEach-Object { $_.Matches.Value } |
    Sort-Object -Unique |
    Where-Object {
        $_ -notmatch '^/wf-(clarify-record|delivery-report|impl-summary|impl-task-matrix|review-checklist|review-summary|phone-sync|docs-mcp)$' -and
        $_ -notmatch 'YYYY-MM-DD'
    }

foreach ($ref in $workflowRefs) {
    Require-Path ("workflows/{0}.md" -f $ref.TrimStart('/'))
}

if ($failures.Count -gt 0) {
    $failures | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Output "Agent-Dev-Kit validation passed: $((Get-ChildItem (Join-Path $KitRoot 'workflows') -Filter 'wf-*.md').Count) workflows checked."
