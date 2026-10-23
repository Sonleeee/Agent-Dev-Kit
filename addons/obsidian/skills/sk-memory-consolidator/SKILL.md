---
name: sk-memory-consolidator
description: Chưng cất bài học, quyết định và root cause từ nội dung phiên do người dùng chỉ định. Dùng khi người dùng yêu cầu tóm tắt hoặc chuẩn bị lưu memory; không tự ghi log từng lượt chat, không tự đọc transcript hay ghi vault.
---

# Memory Consolidator

## Ranh giới

- Chỉ phân tích nội dung phiên, transcript hoặc log mà người dùng chỉ định hoặc đã cho phép truy cập.
- Không tự append từng lượt hội thoại vào `.agents/scratch/current_session.log`.
- Mặc định trả một Memory Candidate để người dùng xem. Chỉ ghi Obsidian khi người dùng yêu cầu lưu rõ hoặc đã thiết lập policy AUTO bền vững.
- Không xóa, truncate hay reset transcript/log sau khi đọc.

## Chưng cất

Giữ lại những nội dung có giá trị tái sử dụng:

- quyết định kiến trúc và lý do lựa chọn;
- root cause, pitfall lặp lại và cách khắc phục;
- convention hoặc quy tắc dự án đã được xác nhận.

Bỏ lời chào, tiến độ tạm, raw output, code nháp thất bại không có bài học, và suy đoán chưa được xác nhận. Không gắn trạng thái `Accepted` cho quyết định nếu người dùng chưa chốt.

## Candidate và lưu trữ

Candidate nên có title, project/source, ngày, tags, bối cảnh, insight/decision và references. Nếu được yêu cầu lưu, dùng [`sk-vault-steward`](../sk-vault-steward/SKILL.md) để tìm vault, kiểm tra file đích và ghi không phá dữ liệu. Mặc định lưu note raw trong `00_Raw/`; chỉ tổng hợp sang Wiki khi được yêu cầu.

Mẫu candidate:

```markdown
---
type: raw_knowledge
project: "{project}"
source: "{session_or_file}"
created: "YYYY-MM-DD"
tags: ["tag1", "tag2"]
---

# {title}

## Context
{bối cảnh và vấn đề}

## Insight
{quyết định, root cause hoặc bài học có thể tái sử dụng}

## References
- {source link}
```

Sau khi ghi, báo chính xác đường dẫn và nội dung đã lưu. Không tuyên bố đã lưu nếu chưa xác minh được file đích.
