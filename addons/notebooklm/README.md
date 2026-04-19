# 🔬 NotebookLM Addon — Research & Synthesis

> Tích hợp NotebookLM để research tài liệu, tổng hợp insights,
> và tạo deliverables (podcast, slide deck, quiz...).

## Vai trò

| Role | Mô tả | Ví dụ |
|------|-------|-------|
| **Research on-demand** | Tìm kiếm tài liệu mới khi cần | "Best practice DDD với .NET 9?" |
| **Knowledge synthesis** | Tổng hợp multi-source thành insight | "So sánh CQRS patterns từ 5 sources" |
| **Artifact generation** | Tạo deliverable từ tri thức | Podcast, slide deck, quiz cho team |
| **Cross-project validation** | So sánh patterns xuyên notebooks | "Architecture hiện tại vs Best Practice?" |

## Setup

1. Cần có NotebookLM MCP server
2. Đăng nhập: `nlm login` (qua terminal)
3. Xem SKILL.md để biết các skills có sẵn
4. Xem workflows/ để biết các workflow có sẵn

## Files

| File | Mô tả |
|------|--------|
| `SKILL.md` | NotebookLM skills (quản trị notebooks, tạo artifacts) |
| `workflows/` | Các workflow chuyên biệt cho NotebookLM |

## Lưu ý

- NotebookLM KHÔNG sync realtime với Obsidian
- Dùng khi cần **research & synthesis**
- Kết quả quan trọng → export vào Obsidian vault thành note vĩnh viễn
