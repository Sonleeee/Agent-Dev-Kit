# 🤖 .agents — Agent-Dev-Kit

> Bộ kit giúp AI agent code đúng pattern, giữ quality gates,
> và tích lũy tri thức dự án. Dùng được trên **mọi IDE/editor** có AI agent.

---

## ⚡ Bắt đầu nhanh (30 giây)

### 1. Clone kit vào project

```bash
# Clone trực tiếp vào thư mục .agents trong dự án của bạn
git clone https://github.com/Sonleeee/Agent-Dev-Kit .agents
```

### 2. Tạo AGENTS.md cho project

```bash
cp .agents/_project-template/AGENTS.md ./AGENTS.md
```

### 3. Điền thông tin project vào AGENTS.md

Mở `AGENTS.md`, điền:
- Tên project
- Tech stack (BE/FE/DB)
- Reference modules

### 4. (Tùy chọn) Tạo project context

```bash
mkdir -p .agents/context
# Copy skeleton templates
cp -r .agents/_project-template/.agents/context/* .agents/context/
```

Điền `architecture.md` với kiến trúc cụ thể của project.

### 5. Cấu hình cho Cursor IDE (Khuyên dùng)

Tạo file `.cursorrules` tại thư mục gốc của project với nội dung:

```markdown
# 🤖 AGENT-DEV-KIT

Trước khi thực hiện bất kỳ task nào, bạn BẮT BUỘC phải:
1. Đọc file `AGENTS.md` ở root directory để hiểu ngữ cảnh dự án.
2. Đọc file `.agents/SYSTEM.md` để nắm các workflow (/wf-clarify, /wf-plan, /wf-impl, /wf-review).
3. Tuân thủ bộ luật tại `.agents/rules/global.md`.
```

---

## 🏗️ Cấu trúc

```
.agents/                          ← Core Kit (clone từ repo)
├── README.md                     ← File này
├── SYSTEM.md                     ← Agent behavior specification
├── rules/
│   └── global.md                 ← Quality gates & guardrails
├── workflows/                    ← 20 workflows (4 nhóm)
├── agents/                       ← 6 system agent personas
├── skills/                       ← 13 skills (6 categories)
│   ├── core/                     ← Discovery, planning, guard, regression
│   ├── meta/                     ← Tạo/cải thiện agent system
│   ├── devops/                   ← CI/CD pipeline, Docker review
│   ├── security/                 ← OWASP scan, secret detection
│   ├── testing/                  ← Test strategy, scenario generator
│   └── research/                 ← Docs seeker, pattern researcher
├── templates/                    ← Output templates
├── quality/                      ← Master checklists
├── registry/                     ← Project type registry
├── _project-template/            ← Template cho project mới
└── addons/                       ← Mở rộng tùy chọn
    ├── swarm/                    ← Multi-agent orchestration
    ├── obsidian/                 ← Second Brain integration
    ├── notebooklm/               ← Research & Synthesis
    └── graphify/                 ← Code structure graph
```

---

## 📋 Workflows (20)

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
| `/wf-delivery` | Full flow: clarify → plan → impl → review |
| `/wf-delivery-lite` | Quick flow cho task đơn giản |
| `/wf-cook` | Auto pipeline: 1 lệnh chạy hết clarify → plan → impl → test → review |

---

## 📋 Registry (Project Types)

Mỗi project type sẽ có bộ quy tắc (rules) và template riêng. Tra danh sách tại `registry/index.md`.


### Utilities

| Lệnh | Mô tả |
|-------|--------|
| `/wf-brainstorm` | So sánh options, trade-off analysis |
| `/wf-enhance` | Refactor/optimize có chủ đích |
| `/wf-deploy` | Deploy checklist |
| `/wf-fix` | Debug pipeline: scout → diagnose → fix → verify → prevent |
| `/wf-test` | Generate & run tests cho module |
| `/wf-docs` | Generate/update documentation |
| `/wf-git` | Git commit messages, PR descriptions, changelog |
| `/wf-scout` | Edge case discovery, error path analysis |
| `/wf-security` | Security scan: OWASP, secrets, auth review |
| `/wf-research` | Research docs, best practices, compare approaches |

### Advanced

| Lệnh | Mô tả |
|-------|--------|
| `/wf-predict` | Expert debate — 5 personas tranh luận impact trước khi implement |
| `/wf-xia` | Port features từ external repos (compare/port/copy/improve) |
| `/wf-retro` | Sprint retrospective — git metrics → health scores → action items |

---

## 🎛️ Mode Modifiers

Thêm flags vào workflows để điều chỉnh hành vi:

```bash
/wf-impl --fast          # Rút gọn, code luôn
/wf-review --red-team    # 4 adversarial personas tấn công code
/wf-predict --focus      # Chỉ chạy personas liên quan
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

## 🔌 IDE/Editor hỗ trợ

Kit hoạt động dựa trên **plain markdown files** + **folder convention**.
Bất kỳ IDE/editor nào có AI agent đọc được file đều dùng được:

| IDE / Editor | AI Agent | Ghi chú |
|---|---|---|
| VS Code | Copilot Chat, Cline | Mainstream |
| Cursor | Built-in (Composer/Chat) | Popular - Dùng kèm `.cursorrules` |
| Windsurf | Cascade | Tương tự Cursor |
| JetBrains | AI Assistant / Copilot | Có thể dùng manual prompt |
| Antigravity | Built-in + MCP | Full support |
| Codex CLI | OpenAI | Terminal-based |
| Gemini CLI | Google | Google ecosystem |
| Vim/Neovim | Copilot / avante.nvim | Power users |

---

## 📦 Addons (Tùy chọn)

Chỉ bật khi cần. Xem `addons/README.md` để biết chi tiết.

| Addon | Mô tả |
|-------|--------|
| `swarm/` | Multi-agent orchestration (fan-out tasks, dual review) |
| `obsidian/` | Tích hợp Obsidian vault làm "bộ não thứ 2" |
| `notebooklm/` | Research & Synthesis với NotebookLM |
| `graphify/` | Code structure graph tự động |

---

## 🧠 Kiến trúc 3 tầng

```
Tầng 3: SECOND BRAIN (tùy chọn)
  Obsidian vault + NotebookLM + Graphify
  Tri thức xuyên projects

Tầng 2: PROJECT LAYER (per-project)
  AGENTS.md + .agents/context/
  Architecture, templates, checklists riêng

Tầng 1: CORE KIT (clone từ repo)
  .agents/ — workflows, rules, quality gates
  Dùng chung cho mọi project
```

---

## 📄 License

MIT License. Tự do sử dụng và tùy biến cho dự án cá nhân và doanh nghiệp.

