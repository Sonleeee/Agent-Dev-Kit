# 🤖 .agents — Agent-Dev-Kit

> Bộ kit giúp AI agent code đúng pattern, giữ quality gates,
> và tích lũy tri thức dự án. Dùng được trên **mọi IDE/editor** có AI agent.

---

## ⚡ Bắt đầu nhanh (1 lệnh duy nhất)

> 🔒 **Lưu ý:** Repo này ở chế độ **Private**. Người dùng cần được cấp quyền Collaborator trên GitHub và máy đã cấu hình SSH Key hoặc Git Credentials.

Mở terminal tại thư mục gốc của dự án và chạy **1 dòng duy nhất**:

**Dùng SSH (Khuyên dùng):**
```powershell
git clone git@github.com:Sonleeee/Agent-Dev-Kit.git .agents; .\.agents\install.ps1 -Full
```

**Hoặc dùng HTTPS:**
```powershell
git clone https://github.com/Sonleeee/Agent-Dev-Kit.git .agents; .\.agents\install.ps1 -Full
```

*(Trên macOS / Linux / Git Bash: thay `; .\.agents\` bằng `&& ./.agents/install.ps1 -Full`)*

> **⚡ Lệnh trên tự động thực hiện 100% (Zero Manual Steps):**
> 1. ✅ Tải Core Kit vào thư mục ngầm `.agents/`.
> 2. ✅ Tự động sinh file `AGENTS.md` tại thư mục gốc dự án.
> 3. ✅ Tự động cập nhật `.gitignore` (bỏ qua `.agents/` và `.codegraph/`).
> 4. ✅ Tự động cài đặt CodeGraph & System Design MCP Server vào IDE và lập chỉ mục AST / Call Graph.
> 5. ✅ Đăng ký lệnh `adk` vào máy — từ dự án thứ hai trở đi bạn chỉ cần gõ: `adk full`.

---

### 🚀 Bắt đầu làm việc ngay với AI

Bạn không cần gọi chuỗi workflow cho task thông thường. Mô tả trực tiếp việc cần làm trong Antigravity hoặc Codex:

```bash
Thêm bộ lọc trạng thái vào trang danh sách đơn hàng. Hãy theo pattern hiện tại,
viết test cho behavior mới, triển khai và chạy kiểm chứng phù hợp.
```

Muốn mở rộng lựa chọn trước khi quyết định, yêu cầu brainstorm. Muốn chỉ làm rõ nghiệp vụ,
lập plan, review độc lập hoặc deploy, hãy nói rõ intent đó hoặc gọi command tương thích.

---

## 🏗️ Cấu trúc

```
.agents/                          ← Core Kit
├── README.md                     ← File này
├── SYSTEM.md                     ← Agent behavior specification
├── rules/
│   └── global.md                 ← Quality gates & guardrails toàn cục

├── agents/                       ← 4 specialist subagents (scout, worker, verifier, critic)
├── skills/                       ← Skills được agent chọn theo intent
│   ├── core/                     ← Discovery, planning, execution contract, regression
│   ├── meta/                     ← Tạo/cải thiện agent system
│   ├── devops/                   ← CI/CD pipeline, Docker review
│   ├── security/                 ← OWASP scan, secret detection
│   ├── testing/                  ← Test strategy, scenario generator
│   └── research/                 ← Docs seeker, pattern researcher, deep research, deep research
├── templates/                    ← Output + execution contract + AGENTS.md templates
├── docs/                         ← Research/rationale và decisions của kit
├── tools/                        ← validate-kit.ps1, evolution_db.py, init-profile.ps1
└── addons/                       ← Addons mở rộng tùy chọn
    ├── codegraph/                ← AST index, call graph, symbols (MCP)
    ├── system-design/            ← Kho kiến trúc chuẩn & scaffold MCP
    ├── obsidian/                 ← Đồng bộ tri thức & web/doc ingestion
    ├── database/                 ← Schema lookup & safe query qua Gridex MCP
    ├── notebooklm/               ← Deep research & synthesis qua NotebookLM
    └── maintainer/               ← Health check & maintenance scripts
```

---

## 🧭 Skill-first, task liền mạch

Với task code đã rõ, coding agent khảo sát phần liên quan, implement, chạy kiểm chứng
phù hợp và rà diff trong cùng phiên. Làm rõ, plan riêng, full review và execution ledger
chỉ bật khi intent, độ phức tạp hoặc rủi ro thực sự cần.

### ⚡ Giao thức giao tiếp mặc định 2 tầng (Dual-Surface Protocol)
ADK mặc định tách bạch ranh giới giữa người và máy:
- **Tầng Ngoài (Human Chat Surface):** Mặc định chạy `adk-adhd-flow` (Action-First, đánh số bước ≤ 5 mục, dòng 1 là hành động, kết thúc < 2 phút, không văn sáo rỗng).
- **Tầng Trong (Subagent Delegation):** Mặc định chạy `adk-caveman` & `adk-compressed-delegation` (Giao thức Cavecrew: nén 60–75% token, giao tiếp máy-máy qua `path:line` và bắt buộc có `verified_cmd`).
- **Tầng Chi tiết (Artifact-First & Adaptive Escape Hatch):** Đẩy full logs/reproduction/case studies vào file contract (`.agents/runtime/<task-id>/...`); tự động mở bung chi tiết khi user yêu cầu mà không cần tắt/bật mode thủ công.

| Ý định | Skill / hành vi |
|---|---|
| Brainstorm và cân nhắc nhiều hướng | `adk-brainstorm`; dừng ở các lựa chọn, không tự chuyển sang plan/code |
| Chốt mục tiêu nghiệp vụ còn mơ hồ | `adk-business-discovery` |
| Lập plan riêng hoặc task có nhiều phụ thuộc | `adk-solution-planning` |
| Technical spec cho thay đổi thiết kế lớn | `adk-sdd` khi user yêu cầu hoặc còn quyết định rủi ro cần chốt |
| Implement task rõ | Làm trực tiếp; TDD khi thay đổi behavior và test phù hợp |
| Debug lỗi chưa rõ nguyên nhân | `adk-systematic-debugging`; bug nhỏ, rõ thì sửa trực tiếp |
| Review độc lập hoặc test riêng | `adk-code-review`, `adk-test-strategy`, `adk-scenario-generator`, `adk-test-authoring` theo yêu cầu |
| Cập nhật docs hoặc soạn nội dung Git | `adk-docs-maintenance`, `adk-git-content` theo intent rõ |

`adk-execution-contract` chỉ dùng cho task nhiều bước, dài qua nhiều lượt, cần resume
hoặc có rủi ro cao. Delegate, worktree và reviewer độc lập là lựa chọn theo lợi ích,
không phải bước bắt buộc.

Source skills được nhóm theo category trong repo. `install.ps1` và `update.ps1` export
từng skill thành thư mục trực tiếp dưới `.agents/skills/<skill-name>/`; khi chạy
`adk addon add <name>`, skill của addon cũng được export theo layout này. Skill trùng
tên với skill riêng của user được giữ nguyên, không bị installer ghi đè.

## 🤖 System Agents (4 Specialist Subagents)

| Subagent | Tool Authority (Inner Harness) | Vai trò & Hợp đồng Đầu ra (Outer Harness) |
|-------|------|--------------|
| `scout` | **Read-Only** (CodeGraph, Grep, Read, Docs) | Khảo sát codebase, trace call graph, khoanh vùng root cause (`path:line`) |
| `worker` | **Scoped Read/Write + Test Runner** | Thực thi thay đổi code/test theo TDD trong phạm vi được giao + `verified_cmd` |
| `verifier` | **Read-Only + Test/Lint/Audit Runner** | Cổng kiểm định độc lập (Fail-Closed Gate: `ADMIT` / `REJECT`), tách biệt khỏi lịch sử chat của Worker |
| `critic` | **Read-Only** (4-Persona Adversarial) | Phản biện đối kháng (Security, Data/State, API, Perf), bẻ gãy giả định ngầm |

> Delegate khi lợi ích vượt chi phí handoff; nếu host không hỗ trợ subagent, xử lý inline theo đúng checklist kiểm định của từng specialist.

---

## 🔌 Môi trường mục tiêu

Kit dùng Agent Skills format và markdown thuần, ưu tiên hai coding agent mà maintainer đang dùng. Invocation thủ công và discovery có khác biệt theo host:

| Môi trường | AI Agent / Engine | Trạng thái | Ghi chú |
|---|---|---|---|
| **Google Antigravity** | Built-in Agent + MCP | Mục tiêu hỗ trợ | Skill có thể tự chọn theo mô tả; slash invocation là đường gọi tường minh của host |
| **Codex (ChatGPT / CLI)** | OpenAI coding agent | Mục tiêu hỗ trợ | Dùng cùng skill format; invocation và UI metadata có thể khác Antigravity |

> Cấu trúc source trong ADK được nhóm theo category; installer export về đường dẫn
> discovery trực tiếp `.agents/skills/<skill-name>/`. Không giả định slash command
> của Antigravity dùng được trên Codex hoặc ngược lại.

---

## 📦 Addons (Tùy chọn)

Chỉ bật khi cần mở rộng tính năng. Xem `addons/README.md` để biết chi tiết.

| Addon | Mô tả | Loại |
|---|---|---|
| [system-design/](./addons/system-design/) | Kho tham khảo kiến trúc và scaffold source base theo yêu cầu | MCP Server / Skill |
| `codegraph/` | Semantic Code Intelligence: lập chỉ mục AST, call graph & symbols (19+ ngôn ngữ) | MCP Server / CLI |
| `obsidian/` | Đồng bộ tri thức hai chiều, web cleaner & document parser cho Obsidian Vault | Vault / Skills |
| `database/` | Tra cứu schema bảng, quan hệ khóa ngoại và query SQL an toàn | Gridex MCP Server |
| `notebooklm/` | Nghiên cứu tài liệu chuyên sâu, đọc tài liệu dày và tổng hợp tri thức | NotebookLM MCP Server |
| `maintainer/` | Bộ công cụ kiểm tra sức khỏe kit (`validate-kit.ps1`) và sinh skill chuẩn | Kit Scripts |

---

---

## 🧠 Kiến trúc 3 tầng phân cấp

```
Tầng 3: DEVELOPER STYLE (cá nhân hóa)
  ~/.agents/developer.md (hoặc .agents/developer.local.md)
  Style code, alias ưa thích, patterns cá nhân mang theo mọi dự án

Tầng 2: PROJECT CONVENTIONS (dự án cụ thể)
  AGENTS.md tại root repo
  Tech stack, architectural patterns, conventions của riêng repo đó

Tầng 1: CORE GUARDRAILS (chuẩn toàn cục)
  .agents/rules/global.md + SYSTEM.md
  Quality gates (Zero-warning, Unit tests 100%, Linters 100%), Invariants
```

---

## 📄 License

MIT License. Tự do sử dụng và tùy biến cho dự án cá nhân và doanh nghiệp.

