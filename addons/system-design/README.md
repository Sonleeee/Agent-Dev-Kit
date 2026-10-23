# System Design Addon

Addon cung cấp kho pattern kiến trúc nội bộ và MCP tool để tra cứu pattern, gợi ý blueprint, hoặc tạo source base khi được yêu cầu.

## Phạm vi

- **Tra cứu/tư vấn kiến trúc:** dùng `sk-system-architect` ở core khi người dùng hỏi về pattern hoặc lựa chọn kiến trúc. Cần bật addon để có các MCP tool `system-design`.
- **Tạo source base:** dùng `sk-system-design-scaffold` chỉ khi người dùng yêu cầu tạo project/source base. Skill kiểm tra thư mục đích trước khi gọi tool.
- **Không tự sinh code:** chỉ nhắc đến một kiến trúc hoặc pattern không có nghĩa là được phép scaffold hoặc inject code.

## Cài đặt

Cài riêng addon:

```powershell
adk addon add system-design
# hoặc
powershell -File .agents/addons/system-design/setup.ps1
```

Cài đặt cấu hình MCP của addon vào các host được setup script hỗ trợ. Xem `setup.js` và `setup.ps1` nếu cần kiểm tra host cụ thể.

## MCP tools

| Tool | Tác dụng |
|---|---|
| `search_patterns`, `get_pattern_details` | Tra cứu pattern từ kho nội bộ |
| `recommend_architecture` | Gợi ý kiến trúc theo tải, team và nghiệp vụ |
| `list_architectures` | Liệt kê blueprint source base |
| `evaluate_interview` | Tính điểm và ghi scratchpad chứa ADR draft vào `project_dir` |
| `scaffold_project` | Ghi source base vào `target_dir` |
| `inject_pattern` | Ghi code pattern vào project hiện có |

`evaluate_interview`, `scaffold_project` và `inject_pattern` có side effect ghi file. Chỉ dùng khi người dùng yêu cầu thao tác tương ứng và đường dẫn đích đã được kiểm tra. `scaffold_project` ghi đè file blueprint mà không kiểm tra xung đột; `inject_pattern` ghi đè `src/patterns/<pattern>.<ext>` nếu trùng tên. Chỉ scaffold trên thư mục mới/rỗng và không inject vào file đã có nội dung cần giữ.

## CLI

```bash
node addons/system-design/mcp-server/index.js search outbox
node addons/system-design/mcp-server/index.js get idempotency-key
node addons/system-design/mcp-server/index.js blueprints
node addons/system-design/mcp-server/index.js scaffold clean-arch-ts ./my-app
```

Lệnh cuối ghi file vào thư mục đích; hãy dùng thư mục mới/rỗng.

## Alias tương thích

`/wf-scaffold` được giữ như adapter deprecated, chỉ dùng khi gọi tường minh. Nó chuyển sang `sk-system-design-scaffold`; procedure chuẩn nằm ở skill, không còn trong workflow.
