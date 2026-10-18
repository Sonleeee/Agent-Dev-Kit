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
> 4. ✅ Tự động cài đặt CodeGraph MCP Server vào IDE và lập chỉ mục AST / Call Graph toàn bộ mã nguồn.
> 5. ✅ Đăng ký lệnh `adk` vào máy — từ dự án thứ hai trở đi bạn chỉ cần gõ: `adk full`.

---

### 🚀 Bắt đầu làm việc ngay với AI

Bạn **không cần phải mở file điền tay**. Hãy mở IDE (Antigravity hoặc Codex CLI) và gõ lệnh chat đầu tiên:

```bash
/wf-clarify "Mô tả tính năng bạn muốn làm..."
```

*(AI Agent sẽ tự động quét mã nguồn dự án, nhận diện tech stack và tự điền thông tin vào `AGENTS.md`).*

---

## 🏗️ Cấu trúc

```
.agents/                          ← Core Kit
├── README.md                     ← File này
├── SYSTEM.md                     ← Agent behavior specification
├── rules/
│   └── global.md                 ← Quality gates & guardrails toàn cục
├── workflows/                    ← 18 workflows (stage, utility, advanced, evolve)
├── agents/                       ← 6 system agent personas
├── skills/                       ← 20 skills (6 categories)
│   ├── core/                     ← Discovery, planning, execution contract, regression
│   ├── meta/                     ← Tạo/cải thiện agent system
│   ├── devops/                   ← CI/CD pipeline, Docker review
│   ├── security/                 ← OWASP scan, secret detection
│   ├── testing/                  ← Test strategy, scenario generator
│   └── research/                 ← Docs seeker, pattern researcher
├── templates/                    ← Output + execution contract + AGENTS.md templates
├── docs/                         ← Research/rationale và decisions của kit
├── tools/                        ← validate-kit.ps1, evolution_db.py, init-profile.ps1
└── addons/                       ← Addons mở rộng tùy chọn
    ├── codegraph/                ← AST index, call graph, symbols (MCP)
    ├── archify/                  ← Interactive HTML visual diagrams
    ├── database/                 ← Schema lookup & safe query qua Gridex MCP
    ├── notebooklm/               ← Deep research & synthesis qua NotebookLM
    └── maintainer/               ← Health check & maintenance scripts
```

---

## 📋 Workflows (23)

### Stage Pipeline (core flow)

| Lệnh | Mô tả | Gate |
|-------|--------|------|
| `/wf-clarify` | Làm rõ requirements | — |
| `/wf-plan` | Lập kế hoạch implementation | Gate 1 |
| `/wf-impl` | Implement code | Gate 2 |
| `/wf-review` | Review 5-layer + ship decision | Gate 3 |

### Shortcuts & Auto-pipeline

| Lệnh | Mô tả |
|-------|--------|
| `/wf-delivery` | Full flow: clarify → plan → impl → review; hỗ trợ `--fast`, `--deep`, `--tdd`, `--auto`, `--parallel` |

### Execution discipline

Mọi task có thay đổi dùng `skills/core/sk-execution-contract/SKILL.md`:

1. Đọc passport, rules và context manifest trước công cụ đầu tiên.
2. Tạo execution contract với objective, scope, acceptance criteria và risk.
3. Ghi progress ledger sau từng phase; task đã `complete` không chạy lại sau compaction.
4. Với task độc lập, subagent mới nhận context tối thiểu và qua hai review: spec compliance, code quality.
5. Chỉ báo `READY` khi có build/test/review evidence.

---



### Utilities

| Lệnh | Mô tả |
|-------|--------|
| `/wf-enhance` | Refactor/optimize có chủ đích |
| `/wf-deploy` | Deploy checklist |
| `/wf-fix` | Debug pipeline: scout → diagnose → fix → verify → prevent |
| `/wf-test` | Generate & run tests cho module |
| `/wf-docs` | Generate/update documentation |
| `/wf-git` | Git commit messages, PR descriptions, changelog |
| `/wf-security` | Security scan: OWASP, secrets, auth review |
| `/wf-research` | Research docs, best practices, compare approaches |

### Advanced

| Lệnh | Mô tả |
|-------|--------|
| `/wf-xia` | Port features từ external repos (compare/port/copy/improve) |
| `/wf-retro` | Sprint retrospective — git metrics → health scores → action items |
| `/wf-vault-sync` | Ghi tri thức đã chưng cất theo writeback policy |

---

## 🎛️ Mode Modifiers

Thêm flags vào workflows để điều chỉnh hành vi:

```bash
/wf-impl --fast          # Rút gọn, code luôn
/wf-review --red-team    # 4 adversarial personas tấn công code
/wf-delivery --tdd       # Test trước rồi implement
/wf-xia --compare        # So sánh kiến trúc, không port code
/wf-retro --churn        # Focus hot spots (files thay đổi nhiều)
```

---

## 🤖 System Agents (6)

| Agent | Role | Khi nào dùng |
|-------|------|--------------|
| `planner` | Lập plan, phân tích scope | `/wf-clarify`, `/wf-plan` |
| `implementer` | Code theo plan, bám sát template | `/wf-impl` |
| `reviewer` | Review 5-layer, ship decision | `/wf-review` |
| `debugger` | Debug root cause, không patch bừa | `/wf-fix` |
| `tester` | Generate tests, coverage analysis | `/wf-test` |
| `red-team` | 4 adversarial personas tấn công code | `/wf-review --red-team` |

> IDE hỗ trợ subagent → tự invoke. IDE không hỗ trợ → user copy persona prompt.

---

## 🔌 Môi trường hỗ trợ (Đã kiểm thử thực tế)

Kit hoạt động dựa trên **plain markdown files** và **quy ước thư mục**, hiện tại được cấu hình, tối ưu hóa và **kiểm thử hoạt động thực tế trên 2 môi trường chính**:

| Môi trường | AI Agent / Engine | Trạng thái | Ghi chú |
|---|---|---|---|
| **Google Antigravity** | Built-in Agent + MCP | ✅ Chính thức (Full support) | Hỗ trợ đầy đủ native workflows, skills, subagents, MCP tools và artifacts |
| **Codex CLI** | OpenAI / Terminal Agent | ✅ Chính thức (Tested) | Thao tác dòng lệnh linh hoạt, nạp context nhanh qua CLI |

> 💡 *Về mặt nguyên lý:* Bất kỳ IDE/editor nào có AI đọc được file (như Cursor, VS Code) đều có thể nạp các quy tắc Markdown này. Tuy nhiên, kit hiện tại chỉ cam kết chất lượng và benchmark chuẩn nhất trên **Antigravity** và **Codex CLI**.

---

## 📦 Addons (Tùy chọn)

Chỉ bật khi cần mở rộng tính năng. Xem `addons/README.md` để biết chi tiết.

| Addon | Mô tả | Loại |
|---|---|---|
| `codegraph/` | Semantic Code Intelligence: lập chỉ mục AST, call graph & symbols (19+ ngôn ngữ) | MCP Server / CLI |
| `archify/` | Biên dịch dữ liệu kiến trúc thành sơ đồ HTML vector tương tác | CLI / Skill |
| `database/` | Tra cứu schema bảng, quan hệ khóa ngoại và query SQL an toàn | Gridex MCP Server |
| `notebooklm/` | Nghiên cứu tài liệu chuyên sâu, đọc tài liệu dày và tổng hợp tri thức | NotebookLM MCP Server |
| `maintainer/` | Bộ công cụ kiểm tra sức khỏe kit (`validate-kit.ps1`) và sinh skill chuẩn | Kit Scripts |

---

## 📓 Tích hợp Second Brain (Obsidian Vault)

Second Brain là kho lưu trữ tài liệu, quyết định kiến trúc (ADR) và bài học dài hạn độc lập ngoài repo:
- **Kết nối:** Khai báo đường dẫn `vault-path` trong file `AGENTS.md` tại root dự án.
- **Chưng cất tri thức:** Chạy workflow `/wf-vault-sync` để tự động nén context, bài học và đồng bộ sang vault (`AUTO/ASK/SKIP`).

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

