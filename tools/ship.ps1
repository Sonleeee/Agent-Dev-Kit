<#
.SYNOPSIS
    ADK Fast Ship: 1-shot add, commit, and push with intelligent multi-tier fallback.
    Zero-dependency, fail-safe: never hangs or fails even if latest-handoff.md is missing.
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Message = ""
)

$ErrorActionPreference = "Stop"

# 1. Stage all changes
git add -A

# Check if there are any staged changes
$staged = git diff --cached --name-only
if (-not $staged) {
    Write-Host "[ADK Ship] Working tree clean. Nothing to commit." -ForegroundColor Yellow
    exit 0
}

# 2. Determine Commit Message via 4-Tier Fallback Cascade
$finalMessage = ""

# Tier 1: User explicitly provided a message
if ($Message.Trim().Length -gt 0) {
    $finalMessage = $Message.Trim()
}

# Tier 2: Read Executive Summary from .agents/runtime/latest-handoff.md if present
if (-not $finalMessage) {
    $handoffFile = Join-Path $PSScriptRoot "..\.agents\runtime\latest-handoff.md"
    if (Test-Path $handoffFile) {
        $content = Get-Content $handoffFile -Raw -Encoding UTF8
        if ($content -match '## 1\. Executive Summary\s*>\s*([^\r\n]+)') {
            $rawSummary = $matches[1].Trim()
            if ($rawSummary.Length -gt 72) {
                $rawSummary = $rawSummary.Substring(0, 69) + "..."
            }
            $finalMessage = "chore(handoff): $rawSummary"
        }
    }
}

# Tier 3: Heuristic inference from staged file paths
if (-not $finalMessage) {
    $files = $staged -split "`r?`n" | Where-Object { $_ -match '\S' }
    $firstFile = Split-Path $files[0] -Leaf

    if ($files.Count -eq 1) {
        $finalMessage = "chore: update $firstFile"
    } elseif (($files | Where-Object { $_ -match '^docs[/\\]|\.md$' }).Count -eq $files.Count) {
        $finalMessage = "docs: update project documentation"
    } elseif ($files | Where-Object { $_ -match '^skills[/\\]' }) {
        $finalMessage = "feat(skills): update agent skills"
    } elseif ($files | Where-Object { $_ -match '^schemas[/\\]|^tools[/\\]' }) {
        $finalMessage = "refactor(core): update schemas and tools"
    } else {
        $finalMessage = "chore: update $firstFile and $($files.Count - 1) other file(s)"
    }
}

# Tier 4: Ultimate Safety Net
if (-not $finalMessage) {
    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm")
    $finalMessage = "chore(auto): update workspace changes ($timestamp)"
}

Write-Host "[ADK Ship] Committing: '$finalMessage'..." -ForegroundColor Cyan
git commit -m $finalMessage

Write-Host "[ADK Ship] Pushing to remote..." -ForegroundColor Cyan
git push

Write-Host "[ADK Ship] Successfully shipped!" -ForegroundColor Green
