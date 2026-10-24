param(
    [string]$KitRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
$failures = [System.Collections.Generic.List[string]]::new()
$warnings = [System.Collections.Generic.List[string]]::new()

function Require-Path([string]$RelativePath) {
    if (-not (Test-Path (Join-Path $KitRoot $RelativePath))) {
        $failures.Add("Missing required file: $RelativePath")
    }
}

@(
    'AGENTS.md', 'SYSTEM.md', 'README.md', 'rules/global.md',
    'templates/execution-contract.md.template',
    'skills/core/adk-execution-contract/SKILL.md',
    'agents/scout/AGENT.md', 'agents/worker/AGENT.md',
    'agents/verifier/AGENT.md', 'agents/critic/AGENT.md'
) | ForEach-Object { Require-Path $_ }

# 1. Validate Skills (Frontmatter, Portable YAML Keys, Description Budget)
$allowedFrontmatterKeys = @('name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools')
$skillRoots = @(
    (Join-Path $KitRoot 'skills'),
    (Join-Path $KitRoot 'addons')
) | Where-Object { Test-Path $_ }
$skillDocs = Get-ChildItem -Path $skillRoots -Recurse -File -Filter 'SKILL.md' |
    Where-Object { $_.Directory.Name -like 'adk-*' }
$skillNames = @{}

foreach ($skillDoc in $skillDocs) {
    $content = Get-Content -Path $skillDoc.FullName -Raw
    $frontmatterMatch = [regex]::Match($content, '(?s)^---\r?\n(?<frontmatter>.*?)\r?\n---(?:\r?\n|$)')
    if (-not $frontmatterMatch.Success) {
        $failures.Add("Invalid skill frontmatter: $($skillDoc.FullName)")
        continue
    }

    $frontmatter = $frontmatterMatch.Groups['frontmatter'].Value
    $nameMatch = [regex]::Match($frontmatter, '(?m)^name:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*$')
    if (-not $nameMatch.Success) {
        $failures.Add("Missing or invalid skill name: $($skillDoc.FullName)")
        continue
    }

    $skillName = $nameMatch.Groups[1].Value
    if ($skillName -ne $skillDoc.Directory.Name) {
        $failures.Add("Skill name '$skillName' does not match folder '$($skillDoc.Directory.Name)'")
    }
    if ($frontmatter -notmatch '(?m)^description:\s*\S') {
        $failures.Add("Missing skill description: $($skillDoc.FullName)")
    }

    # Check top-level frontmatter keys for Agent Skills portability
    $topKeys = [regex]::Matches($frontmatter, '(?m)^([a-zA-Z0-9_-]+):')
    foreach ($tk in $topKeys) {
        $keyName = $tk.Groups[1].Value
        if ($keyName -notin $allowedFrontmatterKeys) {
            $failures.Add("Non-portable frontmatter key '$keyName' in $($skillDoc.FullName)")
        }
    }

    # Check description length budget (warn if > 360 chars to prevent discovery context bloat)
    $descExtract = ($frontmatter -replace '(?m)^name:.*$', '').Trim()
    if ($descExtract.Length -gt 380) {
        $warnings.Add("Long skill description ($($descExtract.Length) chars) in '$skillName' - consider trimming to save discovery tokens.")
    }

    if ($skillNames.ContainsKey($skillName)) {
        $failures.Add("Duplicate skill name '$skillName': $($skillNames[$skillName]) and $($skillDoc.FullName)")
    } else {
        $skillNames[$skillName] = $skillDoc.FullName
    }
}

# 2. Verify that core skills are properly exposed in .agents/skills for 1-level deep host discovery
$agentsSkillsDir = Join-Path $KitRoot '.agents/skills'
if (Test-Path $agentsSkillsDir) {
    $coreSkills = Get-ChildItem -Path (Join-Path $KitRoot 'skills') -Recurse -Directory |
        Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') }
    foreach ($cs in $coreSkills) {
        $exposedPath = Join-Path $agentsSkillsDir $cs.Name
        if (-not (Test-Path $exposedPath)) {
            $failures.Add("Core skill '$($cs.Name)' is not exposed in .agents/skills/")
        }
    }
}

# 3. Check for leftover __pycache__ or .pyc files in working tree
$pycFiles = Get-ChildItem -Path $KitRoot -Recurse -File -Include '*.pyc' -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\\\.git\\' }
if ($pycFiles.Count -gt 0) {
    $failures.Add("Found $($pycFiles.Count) .pyc bytecode file(s) in working tree. Clean up __pycache__.")
}

# 4. Check relative markdown links in core entrypoints (README.md, SYSTEM.md, rules/global.md)
foreach ($entryRel in @('README.md', 'SYSTEM.md', 'rules/global.md')) {
    $entryFull = Join-Path $KitRoot $entryRel
    if (-not (Test-Path $entryFull)) { continue }
    $entryDir = Split-Path -Parent $entryFull
    $text = Get-Content -Path $entryFull -Raw
    $links = [regex]::Matches($text, '\[[^\]]+\]\((?!https?:|mailto:|file:|conversation:|#)(?<target>[^)#\s]+)')
    foreach ($m in $links) {
        $relTarget = $m.Groups['target'].Value
        $resolved = Join-Path $entryDir $relTarget
        if (-not (Test-Path $resolved)) {
            $failures.Add("Broken relative link '$relTarget' in $entryRel")
        }
    }
}

if ($warnings.Count -gt 0) {
    $warnings | ForEach-Object { Write-Warning $_ }
}

if ($failures.Count -gt 0) {
    $failures | ForEach-Object { Write-Error $_ }
    exit 1
}

$coreCount = (Get-ChildItem -Path (Join-Path $KitRoot 'skills') -Recurse -File -Filter 'SKILL.md').Count
$addonCount = $skillDocs.Count - $coreCount
Write-Output "Agent-Dev-Kit validation passed: $($skillDocs.Count) skills checked ($coreCount core, $addonCount addon)."
