# Agent System — Agent-Dev-Kit

Bộ agent dùng chung cho mọi project và mọi platform/IDE.

## Cách hoạt động

```text
.agents/ (KIT — clone từ repo)
    ├── rules/          ← Global rules & Executable gates
    ├── skills/         ← Skills tái sử dụng
    ├── workflows/      ← Các workflow chuẩn (/wf-clarify, /wf-plan, /wf-impl, /wf-review...)
    ├── agents/         ← System agent personas
    ├── templates/      ← Output & Contract templates
    ├── schemas/        ← Database schemas (evolution.db)
    ├── tools/          ← CLI tools (evolution_db.py, validate-kit.ps1)
    ├── config/         ← Config templates
    └── addons/         ← Mở rộng tùy chọn (codegraph, archify, database...)

[project-root]/
    ├── AGENTS.md       ← "Passport" của project (tech stack, conventions, reference modules)
    └── .agents/
        ├── runtime/    ← Execution contracts & task ledgers
        └── developer.local.md ← (Tùy chọn) Override style cá nhân cho riêng repo này

~/.agents/ (User Home)
    └── developer.md    ← Global Developer Profile (Gu code, tone áp dụng cho MỌI repo)
```

## Cách xử lý task

### Đường mặc định

Với yêu cầu đã rõ, xử lý liền mạch trong cùng phiên:

1. Đọc đúng context và phần code liên quan đến yêu cầu.
2. Hỏi làm rõ chỉ khi thiếu quyết định có thể làm đổi kết quả hoặc gây rủi ro đáng kể.
3. Lập plan ngắn trong đầu hoặc trong câu trả lời khi task có nhiều bước; không tạo artifact chỉ để đủ thủ tục.
4. Khi đổi behavior và có test phù hợp, dùng TDD: viết một test thất bại, sửa tối thiểu để pass, rồi refactor nếu cần.
5. Chạy kiểm chứng phù hợp với phạm vi và rà diff một lần trước khi báo kết quả.

Task một bước, dễ kiểm chứng không cần đi qua chuỗi clarify → plan → implement → review.
Không cần thông báo tên skill/workflow trước mỗi hành động; chỉ nêu khi cách tiếp cận ảnh hưởng đáng kể đến người dùng.

### Nạp context và skill

- Đọc `AGENTS.md` cùng `rules/global.md` để hiểu ranh giới và quy ước áp dụng; chỉ nạp thêm context liên quan đến task.
- Đọc `.agents/developer.local.md` hoặc `~/.agents/developer.md` khi chúng có sẵn và ảnh hưởng đến cách thực hiện/giao tiếp.
- Chọn skill theo intent thực tế từ `name` và `description`. Nếu không có skill phù hợp, xử lý trực tiếp; không tìm skill như một bước hình thức.
- Áp dụng communication preset phù hợp (`standard`, `concise`, `adhd-flow`, `caveman`/`ultracave`). Với prompt ngắn, ưu tiên câu trả lời gọn và đưa hành động lên trước.
- Với tác vụ source code, dùng CodeGraph trước khi đọc/tìm source nếu repo có index và CodeGraph khả dụng. Dùng công cụ đọc/tìm thông thường cho docs, config, literal text, git diff/status hoặc file chưa index.

### Execution contract và ledger

`sk-execution-contract` là lựa chọn cho task nhiều bước, dài qua nhiều lượt, cần resume,
có rủi ro cao hoặc có nhiều người/agent cùng làm. Không tạo contract/ledger cho task ngắn,
một bước, phạm vi rõ và kết quả dễ kiểm chứng. Khi đã tạo ledger, cập nhật nó đủ để resume
đúng vị trí; trace capture là best-effort và không được chặn delivery.

### Planning và delegation

- Dùng `sk-solution-planning` khi người dùng yêu cầu plan riêng, task có nhiều nhánh phụ thuộc,
  hoặc approach chưa hiển nhiên. Dùng `sk-sdd` khi cần spec/ADR hoặc thay đổi kiến trúc,
  API hay dữ liệu có ảnh hưởng đáng kể.
- Delegate khi phần việc thực sự độc lập và lợi ích dự kiến lớn hơn chi phí handoff, hợp nhất
  và review. Số file/subtask riêng lẻ không tự tạo nghĩa vụ delegate.
- Reviewer subagent, worktree và multi-agent protocol chỉ dùng khi được yêu cầu hoặc khi rủi ro,
  tính song song và khả năng cô lập làm chúng đáng giá. Không review subtask theo thủ tục.

### Tự kiểm tra và báo kết quả

- Rà diff để tìm thay đổi ngoài ý muốn và lỗi rõ ràng; full review là intent riêng, không phải
  gate bắt buộc sau mọi lần implement.
- Nêu lệnh kiểm chứng đã chạy và kết quả thật. Nếu không chạy được hoặc không phù hợp, ghi rõ;
  không suy diễn test/build pass từ việc code có vẻ đúng.
- Giữ nguyên scope đã yêu cầu. Hỏi user trước hành động có side effect ngoài ý định rõ ràng,
  như deploy, commit/push, ghi dữ liệu vào vault hoặc scaffold source base.

### Minimality checkpoint

Trước khi thêm abstraction/dependency, cân nhắc nhu cầu thực, helper/pattern sẵn có,
standard library/native feature và phương án ít file/state nhất. Không giản lược validation
ở trust boundary, security, accessibility, chống mất dữ liệu hoặc yêu cầu user nêu rõ.

### CodeGraph-First Scout

Khi task cần đọc, hiểu, sửa, review hoặc debug source code và CodeGraph khả dụng:

1. Dùng `mcp__codegraph.codegraph_explore` cho feature/flow/khu vực liên quan.
2. Dùng `mcp__codegraph.codegraph_node` khi đã biết file hoặc symbol cần đọc.
3. Dùng `mcp__codegraph.codegraph_callers` để phân tích impact trước khi đổi behavior,
   signature hoặc contract.
4. Fallback sang `rg`, `Get-Content` hoặc công cụ tương đương cho docs/config/assets,
   literal text, git diff/status hoặc file CodeGraph không index.

Output CodeGraph có source hiện tại được xem như đã đọc file; không đọc lại cùng nội dung
nếu không có lý do rõ ràng.

## Định tuyến theo intent

Skill auto-trigger giúp agent nạp procedure phù hợp; đây không phải pipeline cứng và không
thay đổi phạm vi yêu cầu của user.

| Ý định | Hành vi mặc định |
|---|---|
| Task code đã rõ: thêm, sửa bug, refactor | Thực hiện trực tiếp; TDD khi đổi behavior và test phù hợp; verify theo phạm vi |
| Brainstorm, cần nhiều hướng để cân nhắc | `sk-brainstorm`; kết thúc ở các lựa chọn, không tự sang plan/code |
| Bug chưa rõ nguyên nhân hoặc nhiều layer | `sk-systematic-debugging`; bug hiển nhiên, phạm vi hẹp thì sửa trực tiếp |
| Mục tiêu nghiệp vụ chưa rõ và user muốn chốt yêu cầu | `sk-business-discovery` |
| PRD, Epic, Stories hoặc AC | `sk-agile-ba` |
| User muốn plan riêng hoặc task nhiều nhánh/rủi ro | `sk-solution-planning`; `sk-sdd` cho thiết kế rủi ro cao |
| User yêu cầu review độc lập | `sk-code-review` |
| User yêu cầu test strategy/scenario/test authoring | `sk-test-strategy`, `sk-scenario-generator`, `sk-test-authoring`; TDD vẫn diễn ra trong task sửa code |
| Cập nhật docs theo thay đổi source | `sk-docs-maintenance`; docs/library research dùng `sk-docs-seeker` |
| Pattern hoặc NotebookLM research | `sk-pattern-researcher` hoặc `sk-notebooklm-research` theo nguồn |
| Soạn commit/PR/changelog | `sk-git-content`; commit/push vẫn chỉ khi user yêu cầu rõ |
| Deploy, scaffold, retro, kit evolution, ghi vault | Chỉ khi user yêu cầu intent đó; dùng skill/adapter tương ứng và giữ side-effect guard |

Chỉ hỏi user khi câu trả lời có thể đổi lựa chọn hoặc ranh giới an toàn; nếu không, nêu giả định
và tiếp tục với phạm vi có thể xác định.

## Modifiers theo host

Các file `/wf-*` còn được giữ làm adapter tài liệu trong giai đoạn chuyển đổi. Chỉ host
còn hỗ trợ workflow mới gọi được chúng; dùng intent/skill làm đường portable mặc định.
Workflow stage cũ được thu gọn thành adapter tới skill phù hợp hoặc thao tác trực tiếp.
Modifiers chỉ áp dụng cho workflow nhận chúng; không giả định skill host khác hiểu cú pháp này.

## Nhóm skill

Skills được nạp theo intent qua `name` và `description`; nhóm thư mục chỉ giúp
maintainer sắp xếp source. Không dùng số lượng skill hay category làm router cứng.

| Nhóm | Ví dụ |
|---|---|
| `core/` | brainstorm, business discovery, planning, execution contract, API guard |
| `meta/` | skill synthesis, trace capture, tối ưu agent instructions |
| `devops/` | CI/CD và Docker review |
| `security/` | OWASP, secrets, API contract |
| `testing/` | test strategy và test scenarios |
| `research/` | docs/library lookup, pattern research, NotebookLM research |

Context cache, vault writeback, database inspection, scaffold và kit evolution nằm
trong addons; các side effect chỉ chạy theo intent rõ ràng. Domain skills riêng của
project thuộc project `.agents/skills/` hoặc vị trí mà host hỗ trợ.

## Workflow command còn lại

Các file lệnh dưới đây được giữ làm adapter trong giai đoạn chuyển đổi. Chỉ host còn
hỗ trợ workflow mới gọi được chúng; chúng không định nghĩa đường chạy mặc định. Chỉ
dùng command có side effect khi user yêu cầu rõ.

| Nhóm | Command | Vai trò sau migration |
|---|---|---|
| Alias theo host | `/wf-clarify`, `/wf-plan`, `/wf-impl`, `/wf-delivery` | Lệnh cũ cho host còn hỗ trợ workflow; intent/skill là đường dùng chung |
| Alias theo host | `/wf-review`, `/wf-fix`, `/wf-test`, `/wf-docs` | Gọi procedure chuyên biệt theo intent; không tự chạy sau mỗi lần code |
| Research/security | `/wf-research`, `/wf-security` | Adapter tới skill theo nguồn/phạm vi |
| Side effect | `/wf-git`, `/wf-deploy`, `/wf-scaffold` | Chỉ theo yêu cầu rõ; giữ xác nhận cần thiết trước thao tác |
| Maintainer/analysis | `/wf-status`, `/wf-retro`, `/wf-xia`, `/wf-evolve`, `/wf-enhance` | Lệnh tường minh; không tự kích hoạt sau commit hay delivery |

## Nếu project chưa có AGENTS.md

Agent chạy ở generic mode:

- Dùng global rules
- Hỏi user về context cần thiết
- Gợi ý onboard project bằng `templates/AGENTS.md.template` và khởi tạo `.agents/context/`

## System Agents

Kit cung cấp 6 agent personas trong `agents/`. Mỗi agent là 1 `AGENT.md` chứa persona, skills, và quy trình riêng.

| Agent | Role | Khi nào dùng |
|---|---|---|
| `planner` | Discovery, approach và plan riêng | User yêu cầu plan/discovery hoặc còn quyết định đáng kể |
| `implementer` | Thực thi task code liền mạch | Yêu cầu create/fix/refactor đã rõ |
| `reviewer` | Review độc lập theo risk | User yêu cầu hoặc thay đổi cần góc nhìn thứ hai |
| `debugger` | Điều tra nguyên nhân gốc | Symptom chưa rõ, lỗi nhiều lớp hoặc regression khó cô lập |
| `tester` | Test strategy, test authoring, coverage | User yêu cầu test riêng hoặc cần QA độc lập |
| `red-team` | Phản biện đối kháng | User yêu cầu hoặc risk bảo mật/dữ liệu cao |

**IDE-agnostic:** `AGENT.md` chỉ chứa persona + instructions dạng markdown.
- Host hỗ trợ subagent → delegate khi lợi ích vượt chi phí handoff.
- Host không hỗ trợ → xử lý inline hoặc dùng persona trong hội thoại.
- Swarm setup → xem `addons/swarm/README.md`

## Tiered Context Loading

Khi project có `architecture.md` theo TIER format, agent load theo nhu cầu:

| Tier | Nội dung | Load khi nào | Token ước tính |
|------|---------|-------------|:--------------:|
| **TIER-0** | Core rules, naming, folder, anti-pattern index | Khi task chạm vào phần này | ≤1,000 |
| **TIER-1** | Pattern detail theo [TAG] | Theo task-feature | ~500-1,000 |
| **TIER-2** | Full examples, decision tree, legacy notes | On-demand | ~0-2,000 |

### Loading Protocol

```
1. Đọc đúng TIER-0 rule cần cho task; không nạp toàn bộ architecture mặc định.
2. Xác định task-feature → tìm [TAG] phù hợp → đọc TIER-1 section đó.
3. Chỉ đọc TIER-2 khi:
   - Cần ✅/❌ code examples
   - Cần decision tree cho pattern có variants
   - Cần kiểm tra baseline modules
```

> Nếu `architecture.md` CHƯA theo TIER format → đọc toàn bộ (fallback).

---

## Truth Hierarchy & Resolution

### Truth Resolution Order (Thứ tự chân lý):

1. 🥇 **Executable Verification:** Kết quả build/test/lint thực tế đã chạy phù hợp với phạm vi task.
2. 🥈 **CodeGraph Intelligence:** Đồ thị AST, quan hệ hàm (call graph) và symbol relationships thực tế của codebase.
3. 🥉 **Project Conventions:** File `AGENTS.md` (Passport và reference modules).
4. 🏅 **Developer Profile:** `~/.agents/developer.md` hoặc `.agents/developer.local.md`.

### Khi có xung đột:
- Global Guardrails luôn thắng Project Conventions.
- Project Conventions luôn thắng Developer Personal Style.
- Nếu code thực tế mâu thuẫn với yêu cầu trong task: Trình **Conflict Report** cho user (xem `templates/conflict-report.md.template`).

---

## Addon Hooks

Addon có thể bổ sung skill, command, MCP hoặc hook riêng. Nạp addon chỉ khi intent
cần đến capability đó; xem `addons/<tên>/README.md`.

## Multi-Agent Delegation

Delegation là lựa chọn theo lợi ích dự kiến. Dùng subagent khi task độc lập, có thể
chạy song song hoặc cần góc nhìn chuyên biệt và lợi ích lớn hơn handoff, merge, review.
Không delegate theo số file/subtask cố định và không chạy reviewer sau từng phần theo
thủ tục. Khi host không có subagent, xử lý inline.

Swarm/orchestration nâng cao: xem `addons/swarm/README.md`.
