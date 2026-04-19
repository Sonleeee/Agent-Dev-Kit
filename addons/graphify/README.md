# 📊 Graphify Addon — Code Structure Graph

> Tự động tạo knowledge graph từ codebase,
> giúp agent hiểu cấu trúc code mà không cần grep toàn bộ.

## Tại sao cần?

- **Tiết kiệm tokens**: Agent đọc `GRAPH_REPORT.md` (~1 trang) thay vì scan toàn bộ code
- **Kết nối architecture ↔ code**: Semantic similarity edges
- **God nodes**: Biết ngay đâu là core concepts
- **Auto-sync**: Graph tự update khi code thay đổi

## Setup

1. Cài Graphify
2. Tạo `.graphifyignore` (copy từ `.graphifyignore.example`)
3. Build graph: scan codebase
4. Agent đọc `GRAPH_REPORT.md` khi cần hiểu code structure

## Files

| File | Mô tả |
|------|--------|
| `.graphifyignore.example` | Template ignore file (node_modules, bin, obj...) |

## Kết hợp với Obsidian

- Link `GRAPH_REPORT.md` vào Obsidian vault
- Project brain = `.agents/context/` + Graphify graph
