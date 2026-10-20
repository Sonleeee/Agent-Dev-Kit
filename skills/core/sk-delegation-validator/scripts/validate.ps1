<#
.SYNOPSIS
    Delegation Policy Validator for /wf-impl
.DESCRIPTION
    Kiểm tra execution contract/ledger để verify agent đã tuân thủ
    Delegation Policy. Exit code 1 nếu vi phạm.
.NOTES
    Chạy sau mỗi subtask completion hoặc trước Dev Done.
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$TaskId,
    
    [string]$RuntimeDir = ".agents/runtime"
)

$ErrorActionPreference = "Stop"

$contractPath = Join-Path $RuntimeDir $TaskId "contract.md"
$ledgerPath   = Join-Path $RuntimeDir $TaskId "ledger.md"

# --- Kiểm tra file tồn tại ---
if (-not (Test-Path $contractPath)) {
    Write-Warning "Contract file not found: $contractPath"
    Write-Warning "Skipping validation (no contract to check against)."
    exit 0
}

$contract = Get-Content $contractPath -Raw
$ledger   = if (Test-Path $ledgerPath) { Get-Content $ledgerPath -Raw } else { "" }

# --- Parse số subtasks từ contract ---
$subtaskMatches = [regex]::Matches($contract, '(?m)^\s*-\s*\[[ x]\]\s+Task-\d+')
$subtaskCount   = $subtaskMatches.Count

if ($subtaskCount -lt 2) {
    Write-Output "✅ Delegation check: $subtaskCount subtask(s) — inline mode OK."
    
    # Kiểm tra self-review
    if ($ledger -notmatch 'spec_compliance_review:\s*(PASS|FAIL)') {
        Write-Output "❌ VIOLATION: Inline mode nhưng KHÔNG có spec compliance review trong ledger."
        Write-Output "→ Agent PHẢI tự chạy spec compliance checklist trước khi Dev Done."
        exit 1
    }
    
    Write-Output "✅ Spec compliance review: found in ledger."
    exit 0
}

# --- Subtasks ≥ 2: kiểm tra delegation ---
Write-Output "📋 Found $subtaskCount subtasks — checking delegation compliance..."

$violations = @()

# Check 1: Subagent invocation evidence
if ($ledger -notmatch 'subagent_invoked:\s*true') {
    $violations += "Không có evidence của subagent invocation trong ledger"
}

# Check 2: Spec compliance review
if ($ledger -notmatch 'spec_compliance_review:\s*(PASS|FAIL)') {
    $violations += "Không có spec compliance review"
}

# Check 3: Code quality review
if ($ledger -notmatch 'code_quality_review:\s*(PASS|FAIL)') {
    $violations += "Không có code quality review"
}

# Check 4: No chat history leak
if ($ledger -match 'chat_history_sent:\s*true') {
    $violations += "Chat history đã bị gửi cho subagent (vi phạm Local Brainwash)"
}

# --- Kết quả ---
if ($violations.Count -gt 0) {
    Write-Output ""
    Write-Output "❌ DELEGATION POLICY VIOLATIONS:"
    foreach ($v in $violations) {
        Write-Output "   - $v"
    }
    Write-Output ""
    Write-Output "→ Agent PHẢI quay lại và sửa các vi phạm trước khi tiếp tục."
    exit 1
} else {
    Write-Output "✅ Delegation policy: ALL CHECKS PASSED"
    exit 0
}
