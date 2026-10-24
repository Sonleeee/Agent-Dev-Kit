# Agent System — Agent-Dev-Kit

Bộ agent dùng chung cho mọi project và mọi platform/IDE.

## Cách hoạt động

```text
.agents/ (KIT — clone từ repo)
    ├── rules/          ← Global rules & Executable gates
    ├── skills/         ← Kho Agent Skills tái sử dụng (chuẩn SKILL.md)
    ├── agents/         ← System agent personas
    ├── templates/      ← Output & Contract templates
    ├── schemas/        ← Database schemas (evolution.db)
    ├── tools/          ← CLI tools (evolution_db.py, validate-kit.ps1)
    ├── config/         ← Config templates
    └── addons/         ← Mở rộng tùy chọn (codegraph, system-design, database...)

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
- Với tác vụ source code, dùng CodeGraph trước khi đọc/tìm source nếu repo có index và CodeGraph khả dụng. Dùng công cụ đọc/tìm thông thường cho docs, config, literal text, git diff/status hoặc file chưa index.

### Kiến trúc giao tiếp mặc định 2 tầng (Default Dual-Surface Protocol)

Mặc định toàn hệ thống ADK vận hành theo **Kiến trúc giao tiếp 2 tầng độc lập (Dual-Surface Communication Architecture)** mà không cần người dùng kích hoạt skill thủ công:

1. **Tầng Ngoài (Human Chat Surface — Mặc định `adk-adhd-flow`):**
   - **Dòng 1 là Hành động hoặc Kết quả trực tiếp:** Nêu ngay việc đã/đang làm hoặc câu trả lời chốt ở dòng đầu tiên. Triệt tiêu 100% lời chào, khen câu hỏi, xin phép và phần tóm tắt lặp lại cuối bài.
   - **Đánh số bước tuần tự & Giới hạn nhận thức:** Trình bày theo `1., 2., 3.`, mỗi nhóm tối đa `≤ 5` mục; mỗi mục bắt đầu bằng động từ hành động hoặc `path:line` cụ thể.
   - **Kết thúc bằng 1 việc tiếp theo dưới 2 phút:** Giúp developer duy trì flow làm việc liên tục, không bị nghẽn nhận thức.

2. **Tầng Trong (Subagent Delegation Protocol — Mặc định `adk-caveman` / `adk-compressed-delegation`):**
   - **Giao thức Cavecrew nén 60–75% token:** Khi Agent chính ủy quyền cho các subagent (`scout`, `worker`, `verifier`, `critic`), toàn bộ trao đổi máy-máy bắt buộc dùng văn phong Caveman/Ultracave (fragment, path:line, status tokens).
   - **Bảo toàn Quality Gates:** Subagent tuyệt đối không viết văn giải thích dài dòng, nhưng **BẮT BUỘC** khóa cứng trường bằng chứng thực thi thật (`verified_cmd`), ngăn chặn nguy cơ tràn context của Agent chính.

3. **Tầng Chi tiết & Bằng chứng (Artifact-First & Adaptive Escape Hatch):**
   - **Báo cáo tóm tắt trên Chat:** Nêu lệnh kiểm chứng thực tế và kết quả tóm tắt (`verified_cmd`) ngay trong chat.
   - **Đẩy chi tiết sâu ra Artifact/Contract:** Full stack trace, log kiểm thử dài, so sánh case study đa chiều hoặc benchmark được đẩy vào `.agents/runtime/<task-id>/execution-contract.md` hoặc markdown artifact kèm link bấm trực tiếp.
   - **Tự động mở khóa chi tiết (Deep-Explanation Mode):** Tự động bung đầy đủ phân tích sâu, bảng so sánh và sơ đồ Mermaid (không bị giới hạn 5 mục) mà **không bắt người dùng phải tắt/bật mode thủ công** khi rơi vào:
     - *Yêu cầu tường minh từ User:* Có từ khóa hoặc ý định cần độ sâu (*"chi tiết"*, *"evidence"*, *"giải thích tại sao"*, *"phân tích sâu"*, *"case study"*, *"so sánh"*, *"deep research"*, *"brainstorm"*).
     - *Quyết định Kiến trúc / Nghiệp vụ rủi ro cao:* Lập ADR, Technical Spec (`adk-sdd`), PRD (`adk-agile-ba`) hoặc thay đổi có blast radius lớn.
     - *Điều tra lỗi đa tầng hoặc Audit bảo mật:* Báo cáo Root-Cause Analysis (`adk-systematic-debugging`) hoặc báo cáo lỗ hổng (`adk-owasp-scan`), hoặc khi debug bị fail > 2 lần liên tiếp.
     - *Báo cáo xung đột (Conflict Report):* Khi code thực tế mâu thuẫn với spec cần chốt hướng đi.

> **Tùy chỉnh cá nhân (Overrides):** Người dùng có thể ghi đè phong cách giao tiếp cá nhân (ví dụ: `standard` văn phong đầy đủ, hoặc `ultracave` toàn diện) thông qua `developer.md` hoặc lệnh chat trực tiếp.

### Execution contract và ledger

`adk-execution-contract` là lựa chọn cho task nhiều bước, dài qua nhiều lượt, cần resume,
có rủi ro cao hoặc có nhiều người/agent cùng làm. Không tạo contract/ledger cho task ngắn,
một bước, phạm vi rõ và kết quả dễ kiểm chứng. Khi đã tạo ledger, cập nhật nó đủ để resume
đúng vị trí; trace capture là best-effort và không được chặn delivery.

### Planning và delegation

- Dùng `adk-solution-planning` khi người dùng yêu cầu plan riêng, task có nhiều nhánh phụ thuộc,
  hoặc approach chưa hiển nhiên. Dùng `adk-sdd` khi cần spec/ADR hoặc thay đổi kiến trúc,
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
| Tự chủ trọn gói ("Let him cook", 1 lệnh khép kín) | `adk-cook`; tự động điều phối subagents qua 5 bước đến khi sẵn sàng ship |
| Port, so sánh hoặc tiếp thu pattern từ repo ngoài | `adk-xia`; phân tích reference repo và chuyển giao code theo chuẩn local |
| Brainstorm, cần nhiều hướng để cân nhắc | `adk-brainstorm`; kết thúc ở các lựa chọn, không tự sang plan/code |
| Bug chưa rõ nguyên nhân hoặc nhiều layer | `adk-systematic-debugging`; bug hiển nhiên, phạm vi hẹp thì sửa trực tiếp |
| Mục tiêu nghiệp vụ chưa rõ và user muốn chốt yêu cầu | `adk-business-discovery` |
| PRD, Epic, Stories hoặc AC | `adk-agile-ba` |
| User muốn plan riêng hoặc task nhiều nhánh/rủi ro | `adk-solution-planning`; `adk-sdd` cho thiết kế rủi ro cao |
| User yêu cầu review độc lập | `adk-code-review` |
| User yêu cầu test strategy/scenario/test authoring | `adk-test-strategy`, `adk-scenario-generator`, `adk-test-authoring`; TDD vẫn diễn ra trong task sửa code |
| Cập nhật docs theo thay đổi source | `adk-docs-maintenance`; tra cứu nhanh API/docs library dùng `adk-docs-seeker` |
| So sánh pattern nhanh hoặc Deep Research đa nguồn | `adk-pattern-researcher` (chọn pattern khi code) hoặc `adk-deep-research` (khảo sát chuyên sâu đa nguồn); NotebookLM dùng `adk-notebooklm-research` (thuộc addon `notebooklm`) |
| Soạn commit/PR/changelog | `adk-git-content`; commit/push vẫn chỉ khi user yêu cầu rõ |
| Deploy, scaffold, retro, kit evolution, ghi vault | Chỉ khi user yêu cầu intent đó; dùng skill/adapter tương ứng và giữ side-effect guard |

Chỉ hỏi user khi câu trả lời có thể đổi lựa chọn hoặc ranh giới an toàn; nếu không, nêu giả định
và tiếp tục với phạm vi có thể xác định.

## Nhóm skill

Skills được nạp theo intent qua `name` và `description`; nhóm thư mục chỉ giúp
maintainer sắp xếp source. Không dùng số lượng skill hay category làm router cứng.

| Nhóm | Ví dụ |
|---|---|
| `core/` | brainstorm, business discovery, planning, autonomous cooking (`adk-cook`), execution contract, API guard |
| `meta/` | skill synthesis, trace capture, tối ưu agent instructions |
| `devops/` | CI/CD và Docker review |
| `security/` | OWASP, secrets, API contract |
| `testing/` | test strategy và test scenarios |
| `research/` | docs/library lookup (`adk-docs-seeker`), pattern comparison (`adk-pattern-researcher`), multi-source deep research (`adk-deep-research`), external repo assimilation (`adk-xia`) |

Context cache, vault writeback, database inspection, scaffold và kit evolution nằm
trong addons; các side effect chỉ chạy theo intent rõ ràng. Domain skills riêng của
project thuộc project `.agents/skills/` hoặc vị trí mà host hỗ trợ.

## Ánh xạ lệnh Slash Legacy (`/wf-*`)

Từ bản 0.8.0, kit đã loại bỏ hoàn toàn các file workflow cứng tại root (`workflows/`) để chuyển sang 100% **Skill-First & Intent-Driven**. Người dùng và Agent không cần dùng các lệnh `/wf-*` như các bước thủ tục bắt buộc. 

Nếu người dùng vẫn gõ lệnh slash legacy theo thói quen hoặc host IDE còn giữ alias, hệ thống sẽ tự động ánh xạ sang Intent / Skill tương ứng:

| Lệnh Legacy | Vai trò / Intent chuẩn thay thế | Skill / Cơ chế xử lý |
|---|---|---|
| `/wf-clarify`, `/wf-plan` | Khảo sát & lập kế hoạch khi có yêu cầu | `adk-business-discovery`, `adk-solution-planning` |
| `/cook`, `/wf-cook` | Chế độ tự chủ trọn gói từ đầu đến cuối ("Let him cook") | `adk-cook` |
| `/wf-impl`, `/wf-fix`, `/wf-enhance` | Triển khai code, sửa lỗi hoặc refactor trực tiếp | Thực thi trực tiếp + TDD; `adk-systematic-debugging` |
| `/wf-xia`, `/xia` | Port / đối chiếu mã nguồn từ external repo | `adk-xia` |
| `/wf-review`, `/wf-test`, `/wf-docs` | Review độc lập, tạo test, bảo trì tài liệu | `adk-code-review`, `adk-test-authoring`, `adk-docs-maintenance` |
| `/wf-research`, `/wf-security` | Tra cứu mẫu kiến trúc hoặc quét bảo mật | `adk-pattern-researcher`, `adk-owasp-scan` |
| `/wf-git`, `/wf-deploy`, `/wf-scaffold` | Tạo commit/PR, deploy, scaffold kiến trúc | `adk-git-content`, `adk-system-design-scaffold` |
| `/wf-status`, `/wf-retro`, `/wf-evolve` | Theo dõi tiến độ, tối ưu hóa quy tắc/skill | `adk-execution-contract`, `adk-gepa-lite` |

## Nếu project chưa có AGENTS.md

Agent chạy ở generic mode:

- Dùng global rules
- Hỏi user về context cần thiết
- Gợi ý onboard project bằng `templates/AGENTS.md.template` và khởi tạo `.agents/context/`

## System Agents (4 Specialist Subagents — Harness Architecture)

Kit cung cấp **4 Specialist Subagents** trong `agents/`, được phân tách theo **Ranh giới Quyền Công cụ (Inner Harness / Tool Authority)** và **Hợp đồng Đầu ra Nén có Kiểm chứng (Outer Harness / Proof-First Cavecrew & Fail-Closed Gate)**:

| Subagent | Tool Authority (Inner Harness) | Outer Harness & Vai trò cốt lõi |
|---|---|---|
| `scout` | **Read-Only** (CodeGraph, Grep, Read, Web/Docs) — *Cấm sửa file* | Khảo sát codebase, trace call graph, khoanh vùng root cause và trả về bảng `path:line` cô đọng để giữ sạch context cho Main Agent |
| `worker` | **Scoped Read/Write + Test Runner** (Hỗ trợ cô lập Git Worktree) | Thực thi thay đổi code/test trong phạm vi `files_changed` được giao, áp dụng TDD và trả về `verified_cmd` thực tế |
| `verifier` | **Read-Only + Test/Lint/Audit Runner** — *Cô lập khỏi lịch sử chat của Worker* | Cổng kiểm định độc lập (Fail-Closed Verification Gate theo `arXiv:2605.17998`): chạy test/lint/scanner thực tế và ra phán quyết `ADMIT` hoặc `REJECT` |
| `critic` | **Read-Only** — *4-Persona Adversarial (Security, Data/State, API, Perf)* | Phản biện thiết kế/code, công kích giả định ngầm, tìm lỗ hổng logic/bảo mật và rủi ro kiến trúc trước khi chốt hoặc merge |

### Ánh xạ Vai trò Legacy sang 4 Specialist Subagents

| Vai trò cũ (Legacy) | Cách thức xử lý trong kiến trúc 4 Specialist Subagents |
|---|---|
| `planner` | Main Agent xử lý trực tiếp với `adk-solution-planning` / `adk-sdd` (dùng `scout` nếu cần khảo sát diện rộng trước khi lập plan) |
| `implementer` | `worker` (khi delegate subtask độc lập) hoặc Main Agent thực thi trực tiếp |
| `debugger` | `scout` (khoanh vùng root cause read-only) + `adk-systematic-debugging` |
| `tester` | `verifier` (chạy kiểm định độc lập) hoặc `worker` + `adk-test-authoring` (khi viết test mới) |
| `reviewer` | `verifier` (kiểm định thực thi) kết hợp `critic` (review rủi ro kiến trúc/logic với `adk-code-review`) |
| `red-team` | `critic` (chế độ tấn công đối kháng với `adk-doubt-critic` & `adk-owasp-scan`) |

**IDE-agnostic:** Mỗi `agents/<name>/AGENT.md` định nghĩa rõ Tool Authority, Input/Output Contract (`Proof-First Cavecrew`) và Fail-Closed Gate:
- Host hỗ trợ subagent → delegate khi lợi ích vượt chi phí handoff.
- Host không hỗ trợ → xử lý inline theo đúng checklist kiểm định của từng specialist.
- Swarm/Worktree orchestration → xem `addons/swarm/README.md`.

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
