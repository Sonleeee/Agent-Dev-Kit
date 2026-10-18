---
id: vault-sync
type: addon-bridge
entry-command: /wf-vault-sync
skills-suggested:
  - core/sk-execution-contract
  - addons/obsidian/skills/sk-vault-steward
---

# /wf-vault-sync

**Mục tiêu:** ghi tri thức đã chưng cất vào Obsidian Vault theo policy, không dump chat.

## Routing

- Research/decision: tạo Memory Candidate trước, mặc định `ASK`.
- Root cause, recurring pitfall, architecture evolution đã approved: `AUTO`.
- Status tạm thời/raw output: `SKIP`.

Verify `vault-path` và cấu trúc vault trước khi ghi. Nếu không verify được, report
blocker và không tự tạo đường dẫn mới.
