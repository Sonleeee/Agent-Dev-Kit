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
    'skills/core/sk-execution-contract/SKILL.md'
) | ForEach-Object { Require-Path $_ }

$skillRoots = @(
    (Join-Path $KitRoot 'skills'),
    (Join-Path $KitRoot 'addons')
) | Where-Object { Test-Path $_ }
$skillDocs = Get-ChildItem -Path $skillRoots -Recurse -File -Filter 'SKILL.md' |
    Where-Object { $_.Directory.Name -like 'sk-*' }
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
    if ($skillNames.ContainsKey($skillName)) {
        $failures.Add("Duplicate skill name '$skillName': $($skillNames[$skillName]) and $($skillDoc.FullName)")
    } else {
        $skillNames[$skillName] = $skillDoc.FullName
    }
}

# Verify that core skills are properly exposed in .agents/skills for 1-level deep host discovery
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

if ($failures.Count -gt 0) {
    $failures | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Output "Agent-Dev-Kit validation passed: $($skillDocs.Count) skills checked."
