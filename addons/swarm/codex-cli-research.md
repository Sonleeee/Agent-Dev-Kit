# Codex CLI MCP Research

Tai lieu nay tong hop research ve cach trien khai `codex-cli` thanh MCP server de `Antigravity` co the goi trong agent swarm.

Muc tieu:

- chot huong ket noi
- tong hop tai lieu/nguon
- dua ra config mau
- ghi ro cac luu y thuc te khi dua vao swarm

---

## 1. Ket Luan Ngan

`codex-cli` co the duoc dung theo huong MCP server.

Huong dung de trien khai cho swarm:

- `Antigravity` = MCP client
- `codex-cli` = MCP server cho implement lane
- `gemini-cli` = MCP server cho review lane

Neu trien khai `codex-cli` theo MCP, huong chuan nen la:

```text
command = "codex"
args = ["mcp-server"]
transport = "stdio"
```

Khong nen dung `codex mcp` de chay server mode.

---

## 2. Nhung Gi Research Xac Nhan Duoc

### 2.1. Codex CLI co ho tro MCP

OpenAI docs xac nhan Codex CLI co he MCP commands nhu:

- `codex mcp add`
- `codex mcp list`
- config trong `~/.codex/config.toml`

Dieu nay xac nhan Codex CLI co kha nang lam viec voi MCP ecosystem.

### 2.2. Codex co server mode rieng

Theo cac nguon public da tim duoc, de chay Codex nhu MCP server phai dung:

```bash
codex mcp-server
```

Khong phai:

```bash
codex mcp
```

### 2.3. Da co public config examples

Da co vi du cong khai theo huong:

```toml
[mcp_servers.codex_mcp]
command = "codex"
args = ["mcp-server"]
startup_timeout_sec = 60.0
tool_timeout_sec = 120.0
```

No cho thay huong trien khai thuc te la MCP stdio server.

---

## 3. Nguon Da Dung

### OpenAI docs

- [Docs MCP](https://developers.openai.com/learn/wf-docs-mcp)
- [Codex CLI](https://developers.openai.com/codex/cli)

### GitHub / issue public

- [openai/openai-cookbook issue #2208](https://github.com/openai/openai-cookbook/issues/2208)
- [openai/codex issue #6127](https://github.com/openai/codex/issues/6127)
- [openai/codex issue #6664](https://github.com/openai/codex/issues/6664)
- [openai/codex issue #4496](https://github.com/openai/codex/issues/4496)
- [openai/codex issue #4828](https://github.com/openai/codex/issues/4828)
- [openai/codex issue #6128](https://github.com/openai/codex/issues/6128)

---

## 4. Cach Trien Khai Cho He Thong Cua Ban

Kien truc da chot cua he thong:

- `Antigravity` = orchestrator
- `codex-cli` = implementer
- `gemini-cli` = reviewer

Transport da chot:

- MCP cho `codex-cli`
- MCP cho `gemini-cli`

Vay deployment shape nen la:

```text
antigravity
  -> MCP server codex-cli
  -> MCP server gemini-cli
```

### Mapping lane

#### Implement lane

- command: `codex`
- args: `["mcp-server"]`
- role: implement bounded task

#### Review lane

- `gemini-cli` can expose MCP server rieng cho review
- role: review diff, findings, residual risk

---

## 5. Config Mau

### 5.1. JSON style

```json
{
  "mcpServers": {
    "codex-cli": {
      "transport": "stdio",
      "command": "codex",
      "args": ["mcp-server"]
    },
    "gemini-cli": {
      "transport": "stdio",
      "command": "<gemini-cli-mcp-command>",
      "args": ["<mcp-arg-1>", "<mcp-arg-2>"]
    }
  },
  "routing": {
    "impl": "codex-cli",
    "review": "gemini-cli"
  }
}
```

### 5.2. TOML style

```toml
[mcp_servers.codex-cli]
command = "codex"
args = ["mcp-server"]
startup_timeout_sec = 60.0
tool_timeout_sec = 120.0

[mcp_servers.gemini-cli]
command = "<gemini-cli-mcp-command>"
args = ["<mcp-arg-1>", "<mcp-arg-2>"]
startup_timeout_sec = 60.0
tool_timeout_sec = 120.0
```

---

## 6. Timeout Va Reliability

Day la phan can rat luu y.

### 6.1. Timeout khoi tao

Nen bat dau voi:

- `startup_timeout_sec = 60`

Ly do:

- MCP server co the can khoi dong cham
- Windows va sandbox co the tang startup cost

### 6.2. Tool timeout

Nen bat dau voi:

- `tool_timeout_sec = 120`
hoac
- `tool_timeout_sec = 180`

Khong nen de qua ngan cho implement lane.

### 6.3. Bounded task

Khong gui task qua lon cho `codex-cli` MCP server.

Moi call nen chi gom:

- 1 bounded task
- 1 context ro
- 1 template selection ro

Khong nen nhan 1 call gom:

- clarify
- plan
- code
- review
- verify

---

## 7. Rủi Ro Va Cac Van De Public Da Co

### 7.1. MCP behavior cua Codex van co issue public

Da co issue public lien quan den:

- timeout
- transport close
- per-call sandbox behavior
- behavior khac nhau giua Codex va cac MCP client khac

Nghia la:

- kien truc MCP la dung huong
- nhung khi vao production can test nho truoc

### 7.2. Windows can test rieng

Vi ban dang o Windows / PowerShell, can uu tien test:

- `codex mcp-server` co chay duoc khong
- Antigravity co spawn stdio MCP o Windows on dinh khong
- encoding / transport close co xuat hien khong

### 7.3. Khong nen de reviewer lane block implement lane

Neu `gemini-cli` MCP server timeout:

- implement lane van nen tiep tuc
- `Antigravity` co the tong hop local checks toi thieu

---

## 8. Khuyen Nghi Trien Khai Theo Giai Doan

### Giai doan 1

Dung MCP cho `codex-cli` truoc.

Muc tieu:

- xac nhan `codex mcp-server` chay duoc
- xac nhan Antigravity goi stdio MCP on dinh
- test voi task rat nho

### Giai doan 2

Them `gemini-cli` MCP server cho review lane.

Muc tieu:

- tach role code/wf-review
- khong lam phuc tap implement lane ngay tu dau

### Giai doan 3

Chuan hoa payload contracts:

- implement request
- implement response
- review request
- review response

Va gan vao flow:

```text
/wf-clarify -> /wf-plan -> /wf-impl -> /wf-review
```

---

## 9. Cac Diem Chua Xac Nhan Tuyet Doi

Research hien tai cho thay huong MCP la hop ly va co co so cong khai, nhung van con nhung diem can tu verify tren may cua ban:

- command line MCP cu the cua `codex-cli` tren environment hien tai
- command line MCP cu the cua `gemini-cli`
- ten tool thuc te ma MCP server expose ra
- co can auth/bootstrap them khong
- config file runtime that su cua Antigravity nam o dau

Nghia la:

- kien truc da chot duoc
- config mau da co
- nhung deployment production van can 1 vong test local

---

## 10. Ket Luan

Huong dung cho he thong cua ban la:

- `Antigravity` dung MCP de goi `codex-cli`
- `codex-cli` chay MCP server bang `codex mcp-server`
- `gemini-cli` cung nen vao MCP lane rieng cho review

Config khoi dau hop ly:

- stdio transport
- startup timeout 60s
- tool timeout 120-180s
- task phai bounded

Day la huong phu hop nhat voi agent swarm ma chung ta da chot:

```text
antigravity -> codex-cli -> gemini-cli -> antigravity
```
