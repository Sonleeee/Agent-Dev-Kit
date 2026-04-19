# 🤖 Universal Agent Kit — Cách hoạt động toàn bộ quy trình

## 1. Kiến trúc 3 tầng

```mermaid
graph TB
    subgraph L3["Tầng 3: SECOND BRAIN (tùy chọn)"]
        OBS["📓 Obsidian Vault<br/>Tri thức xuyên projects"]
        NLM["🔬 NotebookLM<br/>Research & Synthesis"]
        GRA["📊 Graphify<br/>Code structure graph"]
    end

    subgraph L2["Tầng 2: PROJECT LAYER (per-project)"]
        AGT["📋 AGENTS.md<br/>Project passport"]
        CTX["📂 .agents/context/<br/>Architecture, templates, checklist"]
    end

    subgraph L1["Tầng 1: CORE KIT (clone từ repo)"]
        SYS["📖 SYSTEM.md<br/>Agent behavior spec"]
        WF["⚡ workflows/<br/>clarify, plan, impl, review"]
        RL["🛡️ rules/global.md<br/>Quality gates"]
        QA["✅ quality/<br/>Master checklist 38 items"]
        REG["📇 registry/<br/>Project type registry"]
        SK["🧰 skills/<br/>Core + Meta skills"]
        TPL["📝 templates/<br/>Output templates"]
    end

    L3 -.->|optional connect| L2
    L2 -->|reads from| L1
```

**Tóm tắt:**

- **Tầng 1 (Core Kit):** Clone từ GitHub — chứa workflows, rules, quality gates. Dùng **chung** cho mọi project.
- **Tầng 2 (Project Layer):** Mỗi project tự tạo — chứa kiến trúc, templates, checklist **riêng** cho project đó.
- **Tầng 3 (Second Brain):** Tùy chọn — Obsidian vault lưu tri thức xuyên projects, NotebookLM research.

---

## 2. Luồng Agent khi nhận task

```mermaid
sequenceDiagram
    actor User
    participant Agent as AI Agent<br/>(bất kỳ IDE nào)
    participant Kit as .agents/<br/>Core Kit
    participant Ctx as .agents/context/<br/>Project Layer

    User->>Agent: "Thêm feature quản lý kho..."
  
    Note over Agent: Bước 1: Đọc Project Identity
    Agent->>Kit: Đọc AGENTS.md → biết project-type
  
    Note over Agent: Bước 2: Tra Registry
    Agent->>Kit: Đọc registry/index.md<br/>→ biết cần load gì
  
    Note over Agent: Bước 3: Load Rules
    Agent->>Kit: Đọc rules/global.md<br/>→ quality gates & guardrails
  
    Note over Agent: Bước 4: Load Context
    Agent->>Ctx: Đọc context/architecture.md<br/>→ biết kiến trúc project
    Agent->>Ctx: Đọc context/templates/<br/>→ code patterns (ground truth)
  
    Note over Agent: Bước 5: Chọn Workflow
    Agent->>Kit: Chọn workflow phù hợp<br/>(clarify/plan/impl/review)
  
    Agent->>User: Thực thi workflow...
```

### Chi tiết từng bước:

| Bước | Agent làm gì    | File đọc                        | Mục đích                                             |
| ------ | ----------------- | --------------------------------- | ------------------------------------------------------- |
| 1      | Đọc passport    | `AGENTS.md`                     | Biết tên project, tech stack, reference modules       |
| 2      | Tra registry      | `registry/index.md`             | Biết project-type → cần load files nào              |
| 3      | Load rules        | `rules/global.md`               | Biết quality gates, guardrails, PROTECTED/OVERRIDABLE  |
| 4a     | Load architecture | `context/architecture.md`       | Biết kiến trúc, anti-patterns, naming conventions    |
| 4b     | Load templates    | `context/templates/be/` `fe/` | Biết code pattern chuẩn (ground truth để sinh code) |
| 4c     | Load checklist    | `context/checklist.md`          | Biết checklist items riêng của project               |
| 5      | Chọn workflow    | `workflows/*.md`                | Thực thi đúng flow cho loại task                    |

---

## 3. Workflow Flow (luồng chính)

### Flow đầy đủ: `/delivery`

```mermaid
flowchart LR
    C["/clarify<br/>Làm rõ"] --> P["/plan<br/>Lập kế hoạch"]
    P --> I["/impl<br/>Implement"]
    I --> R["/review<br/>Review 5 layers"]
  
    C -.->|Gate 0: Đủ thông tin?| P
    P -.->|Gate 1: Ready?| I
    I -.->|Gate 2: Dev Done?| R
    R -.->|Gate 3: Ship Ready?| SHIP["✅ Ship"]
    R -.->|FAIL| FIX["🔧 Fix → Re-review"]
    FIX --> R
```

### Flow rút gọn: `/delivery-lite`

```
clarify-lite (1-2 câu) → plan-lite (approach + files) → /impl → review-lite
```

### Các workflow khác

| Workflow           | Khi nào dùng                           |
| ------------------ | ---------------------------------------- |
| `/clarify`       | Task mơ hồ, cần hỏi đáp            |
| `/plan`          | Chốt approach + template selection      |
| `/impl`          | Code theo plan đã approved             |
| `/review`        | Review 5 layers với tri-state checklist |
| `/delivery`      | Full flow cho task phức tạp            |
| `/delivery-lite` | Shortcut cho task đơn giản            |
| `/enhance`       | Refactor/optimize có chủ đích        |
| `/brainstorm`    | So sánh options khi cần quyết định  |
| `/deploy`        | Deploy checklist                         |

---

## 4. Chi tiết từng Workflow

### 4.1. `/clarify` — Làm rõ requirements

```
Input:  User request (mơ hồ)
Output: Problem statement, scope in/out, risks, edge cases

Agent làm:
1. Hỏi đáp với user → lộ risk/edge cases
2. (Nếu cần) Scan codebase → hiểu pattern hiện tại
3. Xác định: API contract có đổi không?
4. Output: clarify-record
```

### 4.2. `/plan` — Lập kế hoạch

```
Input:  Output từ /clarify
Output: Approach, file list, template selection, quality card

Agent làm:
1. Xác định modules/files bị ảnh hưởng
2. Chọn template từ context/templates/
3. Tạo task breakdown theo thứ tự
4. Tạo Pre-Implementation Quality Card
5. Đánh giá API contract risk
```

> **Gate 1 — Ready:** Không code nếu thiếu problem statement, scope, plan, quality card.

### 4.3. `/impl` — Implement code

```
Input:  Plan đã approved
Output: Code changes, build result, self-check

Agent làm:
1. Load context (AGENTS.md, architecture.md, templates/)
2. Implement code BÁM SÁT template pattern
3. Self-check: đúng template? đúng naming? đúng error handling?
4. Build verification: dotnet build / npm run build
5. Build PASS → sang /review
   Build FAIL → fix, retry (max 3 lần)
```

> **Gate 2 — Dev Done:** Không review nếu build chưa pass, self-check chưa xong.

### 4.4. `/review` — Review 5 layers

```mermaid
flowchart TD
    L1["Layer 1: Checklist Verification<br/>Từng item: PASS/FAIL/UNPLANNED"] --> L2
    L2["Layer 2: Code Existence<br/>Code thực sự tồn tại?"] --> L3
    L3["Layer 3: Architecture Compliance<br/>Code vs template pattern"] --> L4
    L4["Layer 4: Unplanned Code Detection<br/>Code có nhưng KHÔNG trong plan"] --> L5
    L5["Layer 5: Logic & Quality<br/>Business logic + edge cases"]
  
    L5 --> DEC{Ship Decision}
    DEC -->|0 FAIL, 0 UNPLANNED| READY["✅ Ready — Ship"]
    DEC -->|0 FAIL, có UNPLANNED| REVIEW["⚠️ Needs Review"]
    DEC -->|Có FAIL hoặc Critical| BLOCK["❌ Blocked — Fix"]
```

> **Gate 3 — Ship Ready:** Blocked nếu còn Critical finding hoặc FAIL items chưa fix.

---

## 5. Hệ thống Rules (Quality Gates)

### Rules có 2 loại:

| Loại             | Ý nghĩa                                   | Override được?                          |
| ----------------- | ------------------------------------------- | ------------------------------------------ |
| `[PROTECTED]`   | Rule bắt buộc, KHÔNG ai override được | ❌ Không                                  |
| `[OVERRIDABLE]` | Rule mặc định, project CÓ THỂ override | ✅ Qua file `rule-overrides.approved.md` |

### Các nhóm rules:

| Nhóm                       | Loại       | Ví dụ                                                      |
| --------------------------- | ----------- | ------------------------------------------------------------ |
| **Delivery Gates**    | PROTECTED   | Không code nếu thiếu plan, không ship nếu còn Critical |
| **Bugfix Discipline** | PROTECTED   | Phải xác định root cause trước khi fix                 |
| **API Contract**      | PROTECTED   | Không thay đổi API contract ngoài scope                  |
| **Security**          | PROTECTED   | Không commit secrets, không chạy destructive commands     |
| **Architecture**      | OVERRIDABLE | Phân tầng rõ ràng (project có thể override)            |
| **Code Quality**      | OVERRIDABLE | i18n required, no debug logs, minimal change                 |
| **Checklist**         | OVERRIDABLE | Dùng master checklist 38 items (có thể subset)            |

### Luồng override:

```
1. Agent load rules/global.md
2. Agent load context/rule-overrides.approved.md (nếu có)
3. Với mỗi override:
   - Rule [PROTECTED] → ❌ Ignore override, log cảnh báo
   - Rule [OVERRIDABLE] → ✅ Apply override, log
4. Execute với merged rule set
```

---

## 6. Registry — Hỗ trợ nhiều loại project

File `registry/index.md` map `project-type` → files cần load:

| Project Type                     | Context cần                  | Templates           |
| -------------------------------- | ----------------------------- | ------------------- |
| `dotnet-clean-arch`            | architecture.md, checklist.md | templates/be/       |
| `react-vite`                   | architecture.md, checklist.md | templates/fe/       |
| `dotnet-clean-arch+react-vite` | architecture.md, checklist.md | templates/be/ + fe/ |
| `node-express`                 | architecture.md               | templates/be/       |
| `python-fastapi`               | architecture.md               | templates/be/       |
| `generic`                      | (none required)               | (none)              |
| ...                              | ...                           | ...                 |

**Mở rộng:** Thêm project type mới bằng cách thêm row vào bảng + tạo context files tương ứng.

---

## 7. Addons (Tùy chọn)

```mermaid
graph LR
    CORE["🏗️ Core Kit<br/>Workflows + Rules + Quality"] --> OK["✅ Đủ dùng!"]
  
    CORE -.->|optional| SW["🤖 Swarm Addon<br/>Multi-agent orchestration"]
    CORE -.->|optional| OB["📓 Obsidian Addon<br/>Second Brain"]
    CORE -.->|optional| NL["🔬 NotebookLM Addon<br/>Research & Synthesis"]
    CORE -.->|optional| GR["📊 Graphify Addon<br/>Code structure graph"]
```

| Addon                 | Mô tả                                                   | Khi nào cần                  |
| --------------------- | --------------------------------------------------------- | ------------------------------ |
| **swarm/**      | Fan-out tasks cho nhiều agents (Codex, Gemini, OpenCode) | Khi dùng multi-agent setup    |
| **obsidian/**   | Obsidian vault lưu tri thức xuyên projects             | Khi muốn tích lũy knowledge |
| **notebooklm/** | 14 skills research & synthesis                            | Khi cần deep research         |
| **graphify/**   | Tự động tạo code structure graph                      | Khi muốn visualize codebase   |

---

## 8. Onboarding Project Mới (30 giây)

```
Bước 1: Clone kit
  git clone https://github.com/[repo]/agent-kit .agents

Bước 2: Copy template
  cp .agents/_project-template/AGENTS.md ./AGENTS.md

Bước 3: Điền AGENTS.md
  - project-type: dotnet-clean-arch (hoặc type phù hợp)
  - display-name: Tên project
  - tech stack: .NET, React...

Bước 4 (optional): Tạo context
  cp -r .agents/_project-template/.agents/context .agents/context
  → Điền architecture.md với kiến trúc project

Bước 5: Bắt đầu dùng!
  /clarify "Tôi muốn thêm feature X..."
```

---

## 9. Luồng dữ liệu tổng thể

```mermaid
flowchart TD
    USER["👤 User nhập task"] --> AGENT["🤖 AI Agent"]
  
    AGENT --> READ["📖 Đọc context"]
    READ --> AGENTS_MD["AGENTS.md<br/>→ project-type, tech stack"]
    READ --> REGISTRY["registry/index.md<br/>→ cần load gì"]
    READ --> RULES["rules/global.md<br/>→ quality gates"]
    READ --> ARCH["context/architecture.md<br/>→ kiến trúc"]
    READ --> TMPL["context/templates/<br/>→ code patterns"]
  
    AGENT --> CHOOSE["⚡ Chọn Workflow"]
    CHOOSE --> WF{Loại task?}
  
    WF -->|Phức tạp| DELIVERY["/delivery<br/>clarify→plan→impl→review"]
    WF -->|Đơn giản| LITE["/delivery-lite<br/>Nhanh gọn"]
    WF -->|Refactor| ENHANCE["/enhance"]
    WF -->|So sánh| BRAINSTORM["/brainstorm"]
  
    DELIVERY --> GATE["🚦 Quality Gates"]
    LITE --> GATE
    ENHANCE --> GATE
  
    GATE -->|Pass| SHIP["✅ Ship"]
    GATE -->|Fail| FIX["🔧 Fix & Re-review"]
    FIX --> GATE
```

---

## Tóm tắt: Tại sao hệ thống này hoạt động?

| Yếu tố               | Cơ chế                                                            |
| ---------------------- | ------------------------------------------------------------------- |
| **Consistency**  | Templates = ground truth. Agent luôn sinh code đúng pattern.     |
| **Quality**      | 3 gates bắt buộc + 38-item checklist + 5-layer review.            |
| **Flexibility**  | Rules OVERRIDABLE cho phép project customize mà không phá core. |
| **Scalability**  | Registry extensible — thêm project type mới dễ dàng.           |
| **IDE-agnostic** | Plain markdown files — bất kỳ AI agent đều đọc được.      |
| **Progressive**  | Core Kit đủ dùng. Addons chỉ bật khi thực sự cần.           |
