---
name: sk-vault-steward
description: |
  Cầu nối Agent-Dev-Kit ↔ SecondBrain.
  Nhận tri thức từ workflows (bug fix, research, review...) và ghi vào
  Obsidian Vault theo đúng template chuẩn.
context-required: optional
output: Obsidian notes (00_Raw/ + 01_Wiki/ + 02_Brain/log.md)
vault-path: (đọc từ AGENTS.md hoặc hỏi user)
---

# Vault Steward — Ghi Tri Thức Vào SecondBrain

## Mục tiêu

Đảm bảo tri thức phát sinh trong quá trình làm việc (debug, research, review, implement) được lưu trữ bền vững vào SecondBrain Obsidian Vault — không bị mất theo conversation.

## Khi nào được gọi?

Skill này được gọi bởi các workflows qua **Knowledge Checkpoint** (bước cuối) và tuân thủ `SYSTEM.md` → **Brain Writeback Policy**:

| Workflow | Loại tri thức | Hướng xử lý |
|----------|--------------|-------------|
| `/wf-fix` | Root cause analysis, pitfall mới | Hướng A |
| `/wf-delivery` | Tóm tắt implementation, lessons learned | Hướng A |
| `/wf-research` | Research findings, best practices | Hướng A |
| `/wf-review` | Review findings, pattern violations | Hướng A |
| `/wf-retro` | Sprint insights, health metrics | Hướng A |
| `/wf-vault-sync` (Cloud) | NotebookLM content | Hướng B |
| `/wf-vault-sync` (Phone) | iPhone quick captures | Hướng C |

### Writeback Mode

| Mode | Khi dùng | Hành vi |
|------|----------|---------|
| `AUTO` | Workflow đã xác định tri thức high-value theo Brain Writeback Policy | Ghi ngay, sau đó report file đã tạo/cập nhật |
| `ASK` | Tri thức có thể hữu ích nhưng còn cần user duyệt | Trình Memory Candidate, chỉ ghi khi user đồng ý |
| `SKIP` | Không đủ giá trị dài hạn | Không ghi, chỉ report lý do skip |

## Bước 0: Vault Discovery

Agent xác định vault path:
1. Đọc `AGENTS.md` → tìm field `vault-path` (nếu có).
2. Nếu không có → hỏi user: "SecondBrain vault nằm ở đâu?"
3. Verify: check tồn tại `00_Raw/`, `01_Wiki/`, `02_Brain/`.

---

## Hướng A: Workflow-Direct (chính)

> Ghi tri thức từ workflow Agent-Dev-Kit vào vault.

### Input

Agent nhận từ workflow:
- **mode**: `AUTO` | `ASK` | `SKIP`
- **type**: `bugfix` | `research` | `review` | `implementation` | `retro`
- **title**: Tiêu đề ngắn
- **summary**: Tóm tắt tiếng Việt (≤5 câu)
- **content**: Nội dung chi tiết
- **project**: Tên project (từ AGENTS.md)
- **tags**: Danh sách tags liên quan
- **target**: `raw+wiki` | `cache:patterns` | `cache:reviews` | `cache:decisions` | `log-only`

### Flow

```
Bước 0: Mode Gate
  ├─ SKIP → report lý do, không ghi
  ├─ ASK → trình Memory Candidate, chờ user đồng ý
  └─ AUTO → tiếp tục ghi

Bước 1: Tạo Raw Entry
  ├─ File: 00_Raw/01_AI_Agents/{project}_{title_snake_case}.md
  ├─ Format: raw_source_template
  ├─ ID: {type}_{YYYYMMDD}_{sequence}
  └─ Origin: "Agent-Dev-Kit / {workflow_name}"

Bước 2: Tạo/Update Wiki Entry
  ├─ Tìm article liên quan trong 01_Wiki/
  ├─ Nếu CÓ article → append section mới
  ├─ Nếu KHÔNG → tạo article mới theo wiki_article_template
  └─ BẮT BUỘC: link tới raw source trong 🔗 Tài liệu tham khảo

Bước 3: Update Log
  ├─ Append vào 02_Brain/log.md
  └─ Format: "- {date}: [{type}] {title} — {1-line summary}"

Bước 4: Report
  └─ Trả về: "✅ Đã ghi vào SecondBrain: {raw_file}, {wiki_file}"
```

### Template cho Raw Entry

```markdown
# 📄 Source: {title}
- **ID**: `{type}_{YYYYMMDD}_{seq}`
- **Origin**: Agent-Dev-Kit / {workflow_name}
- **Sync Date**: {YYYY-MM-DD}
- **Project**: {project_name}
- **Tags**: {tag1}, {tag2}

---

## 🔍 Tổng quan (Summary)
{summary — tiếng Việt}

## 📝 Nội dung chi tiết (Content)
{content}

---
[[index|Trở về Index]]
```

---

## Hướng B: Cloud-Direct (NotebookLM)

> Đồng bộ nội dung từ NotebookLM notebooks vào vault.

### Flow

```
Bước 1: List notebooks (dùng MCP notebooklm)
Bước 2: Extract sources + artifacts
Bước 3: Tạo Raw Entries (như Hướng A Bước 1)
Bước 4: Synthesis → Wiki Entries
Bước 5: Update Log
```

> Chi tiết: xem `wf-vault-sync.md` Luồng A.

---

## Hướng C: Phone-Direct (iPhone Quick Capture)

> Phân loại và ghi quick captures từ iPhone.

### Flow

```
Bước 1: Quét notebook Inbox + Daily Ops
Bước 2: Phân loại mỗi entry:
  ├─ IDEA/NOTE → 00_Raw/Incoming/
  ├─ TASK → 02_Brain/Task Systems.md
  └─ KNOWLEDGE → Hướng A flow
Bước 3: Update Log
```

> Chi tiết: xem `wf-vault-sync.md` Luồng B.

---

## Guardrails

- **Ngôn ngữ**: Luôn viết tóm tắt bằng **Tiếng Việt**. Nội dung kỹ thuật có thể giữ Tiếng Anh.
- **Wikilinks**: Sử dụng `[[...]]` cho mọi thực thể. Note không có link = "lỗi hệ thống".
- **Không ghi đè**: Nếu file đã tồn tại → append, không overwrite.
- **Traceability**: Mọi Wiki entry PHẢI link về Raw source.
- **Mode-aware**: `AUTO` được ghi ngay theo policy; `ASK` phải hỏi user; `SKIP` không ghi.
- **Không ghi rác**: Không lưu raw command output, progress tạm thời, hoặc failed attempt không có lesson rõ.
- **Scope**: Focus 100% vào Kiến trúc AI Agent (theo AI_INSTRUCTIONS.md §5). Nội dung ngoài scope → Archive.
