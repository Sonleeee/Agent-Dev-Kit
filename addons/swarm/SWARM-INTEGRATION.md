# Swarm Integration & Contracts

Tai lieu nay chot naming, role mapping, data contract, va routing rules cho he thong.
Transport chuan: MCP + Terminal.

---

## 1. Canonical Naming

Chi dung cac ten nay trong repo:

| Role | Canonical name | Transport |
|---|---|---|
| Orchestrator | `antigravity` | — |
| Implementer #1 | `codex-cli` | MCP |
| Implementer #2 | `gemini-cli` | MCP (`gemini_run_task`) |
| Implementer #3 | `opencode-cli` | Terminal cmd |
| Reviewer (primary) | `codex-cli` | MCP |
| Reviewer (secondary) | `gemini-cli` | MCP (`gemini_review_quality`) |
| Knowledge | `notebooklm` | MCP |

Khong dung lai cac ten mo ho:

- `gemini-swarm`
- `executor`
- `subagent #1` / `subagent #2`
- `review_quality tool`
- `run_task tool`

---

## 2. Canonical Flow

### Serial (default):
```text
/sk-clarify -> /sk-plan -> /sk-impl -> /sk-review
```

### Parallel (khi impl co nhieu task):
```text
/sk-clarify -> /sk-plan -> /sk-impl (fan-out 3 agents) -> build verify -> /sk-review
```

## 2.1. Transport

- `antigravity` -> MCP server `codex-cli`
- `antigravity` -> MCP server `gemini-cli` (`gemini_run_task` + `gemini_review_quality`)
- `antigravity` -> Terminal command `opencode-cli` (non-interactive)
- `antigravity` -> MCP server `notebooklm`

Config mau:

- `integration/mcp-servers.example.json`
- `integration/swarm.config.example.json`

---

## 3. Routing Rules

### `antigravity`

Lam:

- clarify (+ delegate research cho codex-cli khi can)
- plan (+ delegate draft cho codex-cli khi can)
- gate
- tao task matrix + assignment
- fan-out parallel tasks
- build verification (auto detect paths)
- route sang reviewer(s)
- tong hop ket qua
- ship decision

### `codex-cli`

Lam:

- doc project context
- doc project templates
- implement bounded BE/logic task
- self-check
- research codebase (cho /sk-clarify)
- draft plan (cho /sk-plan)
- structured 4-layer review (reviewer chinh)

Khong lam:

- rewrite scope
- sua file da assign cho agent khac

### `gemini-cli`

Lam:

- implement bounded FE/design task (qua `gemini_run_task`)
- parallel overflow khi codex-cli ban
- dual review (qua `gemini_review_quality`) khi task nhieu

Khong lam:

- reviewer mac dinh khi task it
- sua file da assign cho agent khac

### `opencode-cli`

Lam:

- implement bounded parallel task (qua terminal non-interactive)
- backup khi codex-cli hoac gemini-cli bi block

Khong lam:

- reviewer
- research
- sua file da assign cho agent khac

Provider: OpenCode Zen — MiniMax M2.5 Free

---

## 4. File Conflict Policy

> **RULE BAT BUOC:** Khong co 2 agents cung sua 1 file.

### Cross-agent dependency:

Khi agent A can goi function ma agent B tao:

- Rang buoc ten function/class dung
- Rang buoc parameters dung type + thu tu
- **KHONG cho nhau** — moi agent implement doc lap theo contract
- Anti ghi ro cross-agent contracts trong task matrix

Vi du:
```
Agent A (codex-cli) tao: WarehouseService.CreateAsync(dto)
Agent B (gemini-cli) goi: WarehouseService.CreateAsync(dto) trong component
-> Chi can ten + params dung, KHONG can cho A xong moi bat dau B
```

---

## 5. Payload Contracts

### 5.1. Implement Request (codex-cli / gemini-cli)

```json
{
  "agent": "codex-cli | gemini-cli",
  "role": "implementer",
  "task": "short bounded task",
  "scope": "BE | FE | BE+FE",
  "assigned_files": ["path/a", "path/b"],
  "project_context": {
    "agents_md": "required",
    "architecture_md": "required",
    "templates": "required when present",
    "checklist": "optional"
  },
  "plan": {
    "approach": "short chosen approach",
    "files": ["path/a", "path/b"],
    "template_selection": ["template/a", "template/b"],
    "test_obligations": ["item 1", "item 2"]
  },
  "cross_agent_contracts": [
    {
      "depends_on_agent": "codex-cli",
      "function": "ServiceName.MethodName",
      "params": "type1, type2",
      "return_type": "ResultType"
    }
  ]
}
```

### 5.2. Implement Request (opencode-cli — terminal)

```
opencode -p "
Task: [bounded task description]
Files: [assigned files only]
Template: [template path to follow]
Contract: [cross-agent func names + params if any]
Constraint: Chi sua files da assign, khong sua file khac.
" --non-interactive
```

### 5.3. Implement Response

```json
{
  "agent": "codex-cli | gemini-cli | opencode-cli",
  "status": "DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED",
  "changed_files": ["path/a", "path/b"],
  "self_check": ["passed item 1", "passed item 2"],
  "api_contract": "OK | Risk",
  "cross_agent_exports": [
    {
      "function": "ServiceName.MethodName",
      "params": "type1, type2",
      "file": "path/to/file"
    }
  ],
  "assumptions": ["item 1"],
  "blockers": ["item 1"]
}
```

### 5.4. Review Request

```json
{
  "agent": "codex-cli",
  "role": "reviewer",
  "review_mode": "single | dual",
  "scope": "BE | FE | BE+FE",
  "changed_files": ["path/a", "path/b"],
  "task_matrix": "path to task matrix",
  "impl_checklist": ["item 1", "item 2"],
  "cross_agent_contracts": ["contract 1", "contract 2"],
  "architecture_rules": "path to architecture.md",
  "checklist_subset": ["item 1", "item 2"]
}
```

### 5.5. Review Response (tri-state)

```json
{
  "agent": "codex-cli",
  "review_layers": {
    "checklist_verification": [
      {"item": "item 1", "status": "PASS | FAIL | UNPLANNED", "evidence": "file:line"}
    ],
    "code_existence": [
      {"expected": "description", "exists": true, "location": "file:line"}
    ],
    "architecture_compliance": [
      {"rule": "template rule", "compliant": true, "detail": "explanation"}
    ],
    "unplanned_code": [
      {"found": "description", "in_plan": false, "in_template": false, "verdict": "UNPLANNED"}
    ],
    "cross_agent_contracts": [
      {"from": "agent A", "to": "agent B", "function": "name", "params_match": true}
    ]
  },
  "summary": {
    "pass_count": 0,
    "fail_count": 0,
    "unplanned_count": 0
  },
  "ship_decision": "Ready | Blocked | Needs Review"
}
```

---

## 6. Timeout & Fallback Policy

### Implement lane

- neu `codex-cli` bi `NEEDS_CONTEXT` -> quay lai `antigravity` bo sung
- neu `codex-cli` bi `BLOCKED` -> tach nho task hoac route sang `opencode-cli`
- neu `gemini-cli` bi block -> route sang `opencode-cli` hoac `antigravity` tu impl
- neu `opencode-cli` bi block -> `antigravity` tu impl

Fallback chain:
```
codex-cli -> gemini-cli -> opencode-cli -> antigravity tu lam
```

### Review lane

- neu `codex-cli` review timeout -> `antigravity` van tong hop local checks
- dual review (gemini) timeout -> chi dung codex-cli review
- review failure khong duoc lam sap implement lane

### Build verification

- Build FAIL -> Anti phan tich error, route fix cho codex-cli
- Retry build sau fix
- Max 3 retries, sau do bao User

---

## 7. Config Ownership

File config mau cua he `.agents` nam o:

- `integration/swarm.config.example.json`
- `integration/mcp-servers.example.json`

Day la source of truth cho naming va role mapping.

---

## 8. Template Mapping

| Workflow | Output | Template |
|---|---|---|
| `/sk-clarify` | `clarify-record` | `templates/sk-clarify-record.md.template` |
| `/sk-plan` | `implementation-plan-lite` | `templates/implementation-plan-lite.md.template` |
| `/sk-impl` | `impl-summary` | `templates/sk-impl-summary.md.template` |
| `/sk-impl` (parallel) | `impl-task-matrix` | `templates/sk-impl-task-matrix.md.template` |
| `/sk-review` | `review-summary` | `templates/sk-review-summary.md.template` |
| `/sk-review` (checklist) | `review-checklist` | `templates/sk-review-checklist.md.template` |
| `/sk-delivery` | `delivery-report` | `templates/sk-delivery-report.md.template` |

---

## 9. Lich Su Refactor

### Van de he thong cu (da fix):

- flow qua dai (6 buoc), nhieu buoc chong nghia
- `/sk-impl` om qua nhieu trach nhiem
- role implement va review chua tach ro
- Gemini vua code vua review
- project templates chua duoc dua vao trung tam
- output/report qua formal

### Files da xoa o refactor truoc:

- `AGENTIC-WORKFLOW-V2.md`
- `workflows/biz-research.md`, `workflows/solution.md`, `workflows/solution-plan.md`, `workflows/preview.md`
- `templates/quality-gate-card.md.template`, `templates/solution-record.md.template`

### Files da archive o refactor v2.0 (lan nay):

- `AGENTIC-WORKFLOW.md` -> `_archive/`
- `AG_GEMINI_COORDINATION.md` -> `_archive/`
- `MCP-TRANSPORT-ARCHITECTURE.md` -> `_archive/`
- `SWARM-IMPLEMENTATION-SUMMARY.md` -> `_archive/`

---

## 10. Nguyen Tac Van Hanh

De khong bi tro lai he thong cu:

1. Khong tao lai `solution` va `solution-plan` thanh stage bat buoc
2. `gemini-cli` la implementer #2, KHONG phai sole reviewer
3. `codex-cli` la reviewer chinh voi structured checklist
4. Khong bo qua project templates trong `/sk-impl`
5. Khong mo rong report/template theo huong bang bieu dai va formal
6. Khong de utility workflow bien thanh main path
7. File conflict: **bat buoc tach file**, khong co 2 agents cung sua 1 file
8. Cross-agent dependency chi qua contract (func name + params)

---

> Tai lieu nay gop noi dung tu: SWARM-IMPLEMENTATION-SUMMARY.md.
> File goc da duoc archive vao `_archive/`.
