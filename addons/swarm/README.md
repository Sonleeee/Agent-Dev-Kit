# 🤝 Swarm Addon — Multi-Agent Orchestration

> Addon này cho phép fan-out tasks cho nhiều AI agents song song,
> với file conflict policy và cross-agent contracts.

## Khi nào cần?

- Bạn dùng 2+ agents (ví dụ: Codex CLI + Gemini CLI + OpenCode)
- Bạn muốn implement song song (BE agent + FE agent)
- Bạn cần structured dual review

## Files trong addon này

| File | Mô tả |
|------|--------|
| `SWARM-INTEGRATION.md` | Contracts, routing rules, payload formats |
| `mcp-servers.example.json` | Config mẫu cho MCP servers |
| `swarm.config.example.json` | Config mẫu cho swarm orchestration |
| `skills/orchestration/` | Skills cho delivery orchestrator + review workflow |

## Setup

1. Cấu hình MCP servers theo `mcp-servers.example.json`
2. Cấu hình swarm theo `swarm.config.example.json`
3. Đọc `SWARM-INTEGRATION.md` để hiểu routing rules
4. Trong workflows, các note `[Multi-agent]` sẽ trỏ về addon này

## Quy tắc cốt lõi

- **KHÔNG 2 agents sửa cùng 1 file**
- Cross-agent dependency chỉ qua contract (func name + params)
- Agents implement độc lập, không chờ nhau
- Build verification sau khi tất cả agents hoàn tất
