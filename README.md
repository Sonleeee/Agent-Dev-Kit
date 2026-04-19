# 🤖 .agents — Universal Agent Kit

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
# 🤖 UNIVERSAL AGENT KIT

Trước khi thực hiện bất kỳ task nào, bạn BẮT BUỘC phải:
1. Đọc file `AGENTS.md` ở root directory để hiểu ngữ cảnh dự án.
2. Đọc file `.agents/SYSTEM.md` để nắm các workflow (/clarify, /plan, /impl, /review).
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
├── workflows/                    ← /clarify, /plan, /impl, /review...
├── templates/                    ← Output templates
├── quality/                      ← Master checklists
├── registry/                     ← Project type registry
├── skills/
│   ├── core/                     ← Discovery, planning, guard
│   └── meta/                     ← Cải thiện agent system
├── _project-template/            ← Template cho project mới
└── addons/                       ← Mở rộng tùy chọn
    ├── swarm/                    ← Multi-agent orchestration
    ├── obsidian/                 ← Second Brain integration
    ├── notebooklm/               ← Research & Synthesis
    └── graphify/                 ← Code structure graph
```

---

## 📋 Workflows

| Lệnh | Mô tả | Khi nào dùng |
|-------|--------|--------------|
| `/clarify` | Làm rõ requirements | Task mơ hồ, cần hỏi đáp |
| `/plan` | Lập kế hoạch implementation | Chốt approach + template |
| `/impl` | Implement code | Code theo plan |
| `/review` | Review & verify | Kiểm tra 5 layers |
| `/delivery` | Full flow (clarify→plan→impl→review) | Task phức tạp |
| `/delivery-lite` | Shortcut nhanh | Task đơn giản, rõ ràng |
| `/enhance` | Refactor/optimize | Cải thiện code có chủ đích |
| `/brainstorm` | So sánh options | Cần quyết định hướng đi |

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

