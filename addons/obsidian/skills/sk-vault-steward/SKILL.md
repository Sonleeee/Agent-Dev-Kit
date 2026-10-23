---
name: sk-vault-steward
description: Soạn hoặc lưu tri thức đã chưng cất vào Obsidian Vault khi người dùng yêu cầu lưu, ghi note hoặc đồng bộ rõ ràng. Dùng để xác định vault, chọn vị trí và ghi không phá dữ liệu; không tự ghi sau mỗi lần code, research, review hay khi chỉ phát hiện thông tin có vẻ hữu ích.
---

# Obsidian Vault Steward

## Ranh giới ghi

- Đọc, tìm kiếm hoặc chuẩn bị Memory Candidate không tự cho phép ghi file.
- Ghi chỉ khi người dùng yêu cầu lưu/ghi/đồng bộ trong lượt hiện tại, hoặc đã thiết lập một chính sách `AUTO` bền vững và rõ ràng trước đó.
- `ASK`: trình Memory Candidate và chờ người dùng đồng ý.
- `SKIP`: không ghi; nêu ngắn lý do nếu hữu ích.
- Không suy ra quyền ghi từ một workflow hoàn tất, giá trị tri thức, hoặc tên skill được kích hoạt.

## Xác định vault và nội dung

1. Khi cần ghi, đọc `AGENTS.md` để tìm `vault-path`; nếu không có, hỏi đường dẫn vault.
2. Xác nhận vault tồn tại và các thư mục đích đã có. Không tự tạo vault, cây thư mục hay đường dẫn thay thế.
3. Nếu có `AI_INSTRUCTIONS.md` hoặc quy tắc riêng trong vault, đọc và làm theo scope đó.
4. Chưng cất nội dung thành title, summary ngắn, details có giá trị lâu dài, project/source và tags. Không dump hội thoại, tiến độ tạm, raw output hay failed attempt không có bài học.
5. Nếu người dùng chỉ muốn ghi nhận candidate, dừng trước khi ghi.

## Ghi không phá dữ liệu

- Raw knowledge: `00_Raw/01_AI_Agents/` hoặc `00_Raw/Incoming/` khi phù hợp với cấu trúc vault hiện có.
- Wiki: chỉ tạo/cập nhật `01_Wiki/` khi người dùng yêu cầu tổng hợp hoặc synthesis; link rõ về raw source.
- Task từ NotebookLM: dùng vị trí task đã cấu hình, thường là `02_Brain/Task Systems.md`.
- Đọc file đích trước khi sửa. Không overwrite nội dung hiện có; append hoặc cập nhật mục nhỏ sau khi kiểm tra trùng lặp.
- Duy trì wikilinks và traceability về nguồn. Viết phần tóm tắt bằng tiếng Việt; thuật ngữ kỹ thuật có thể giữ tiếng Anh.
- Nếu không xác định được file đích, quyền ghi, hoặc cách xử lý xung đột, dừng và hỏi thay vì tự tạo cấu trúc mới.

Với knowledge note, giữ metadata và cấu trúc ngắn dưới đây; chỉ cập nhật `02_Brain/log.md` nếu file đã tồn tại hoặc người dùng yêu cầu tạo/cập nhật log:

```markdown
---
type: raw_knowledge
project: "{project}"
source: "{source_or_session}"
created: "YYYY-MM-DD"
tags: ["tag1", "tag2"]
---

# {title}

## Summary
{summary}

## Insight
{decision, root cause, or reusable lesson}

## References
- [[{source_note_or_project}]]
```

## Đồng bộ từ NotebookLM

Khi người dùng yêu cầu đồng bộ nội dung NotebookLM, dùng procedure phù hợp trong addon NotebookLM. Với tác vụ gộp iPhone Inbox và Daily Ops, dùng `sk-notebooklm-phone-sync` nếu skill đó được cài/discover; nếu không, giữ ở preview. Nếu MCP NotebookLM chưa bật, báo blocker và không giả lập dữ liệu.

Sau khi ghi, báo chính xác file đã tạo/cập nhật và phần nào bị bỏ qua. Không tuyên bố sync hoàn tất nếu chưa xác nhận nội dung trên đĩa.
