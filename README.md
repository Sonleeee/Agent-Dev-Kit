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
cp .agents/templates/AGENTS.md.template ./AGENTS.md
```

### 3. Điền thông tin project vào AGENTS.md

Mở `AGENTS.md`, điền:
- Tên project
- Tech stack (BE/FE/DB)
- Reference modules

### 4. Khởi tạo CodeGraph (Semantic Code Intelligence)

Kit sử dụng CodeGraph để phân tích call graph, AST và symbol relationships thay cho việc tạo sơ đồ source map thủ công:

```bash
npx @colbymchenry/codegraph
codegraph init -i
```

Sau khi khởi tạo, agent sẽ tự động truy vấn CodeGraph khi làm việc.

### 5. Cấu hình cho Cursor IDE (Khuyên dùng)

Tạo file `.cursorrules` tại thư mục gốc của project với nội dung:

```markdown
# 🤖 AGENT-DEV-KIT

Trước khi thực hiện bất kỳ task nào, bạn BẮT BUỘC phải:
1. Đọc file `AGENTS.md` ở root directory để hiểu ngữ cảnh dự án.
2. Đọc file `.agents/SYSTEM.md` để nắm các workflow (/wf-clarify, /wf-plan, /wf-impl, /wf-review).
3. Nếu có, đọc `.agents/context/manifest.md` để chọn context TIER-1/TIER-2.
4. Tạo execution contract cho task có thay đổi và tuân thủ `.agents/rules/global.md`.
```

---

## 🏗️ Cấu trúc

```
.agents/                          ← Core Kit (clone từ repo)
├── README.md                     ← File này
├── SYSTEM.md                     ← Agent behavior specification
├── rules/
│   └── global.md                 ← Quality gates & guardrails
├── workflows/                    ← 17 workflows (stage, utility, advanced)
├── agents/                       ← 6 system agent personas
├── skills/                       ← 20 skills (6 categories)
│   ├── core/                     ← Discovery, planning, guard, regression
│   ├── meta/                     ← Tạo/cải thiện agent system
│   ├── devops/                   ← CI/CD pipeline, Docker review
│   ├── security/                 ← OWASP scan, secret detection
│   ├── testing/                  ← Test strategy, scenario generator
│   └── research/                 ← Docs seeker, pattern researcher
├── templates/                    ← Output + execution contract templates
├── quality/                      ← Master checklists
├── docs/                         ← Research/rationale và decisions của kit
├── tools/                        ← Kiểm tra consistency của kit
└── addons/                       ← Mở rộng tùy chọn
    ├── swarm/                    ← Multi-agent orchestration
    ├── obsidian/                 ← Second Brain integration
    ├── notebooklm/               ← Research & Synthesis
    ├── archify/                  ← Architecture HTML artifacts
    ├── knowledge/                ← Context cache, memory, vault writeback
    ├── database/                 ← Database/schema inspection
    └── maintainer/               ← Kit maintenance skills
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

## 📋 Registry (Project Types)

Mỗi project type sẽ có bộ quy tắc (rules) và template riêng. Tra danh sách tại `registry/index.md`.


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
| `archify/` | Architecture/workflow HTML artifacts |

---

## 🧠 Kiến trúc 3 tầng

```
Tầng 3: SECOND BRAIN (tùy chọn)
  Obsidian vault + NotebookLM + Archify artifacts
  Tri thức xuyên projects

Tầng 2: PROJECT LAYER (per-project)
  AGENTS.md + .agents/context/
  Manifest (L0), architecture/tags (L1), examples (L2)

Tầng 1: CORE KIT (clone từ repo)
  .agents/ — workflows, rules, quality gates, execution contract
  Dùng chung cho mọi project
```

---

## 📄 License

MIT License. Tự do sử dụng và tùy biến cho dự án cá nhân và doanh nghiệp.

