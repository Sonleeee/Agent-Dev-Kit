# Đối chiếu các repo bên ngoài và quyết định cập nhật kit

Ngày rà soát: 2026-09-07

## Kết luận ngắn

Agent-Dev-Kit đã có pipeline và quality gates, nhưng còn thiếu lớp thực thi luôn
được kiểm tra lại: context manifest, task ledger, skill routing trước hành động,
subtask review và evidence-based completion. Bản cập nhật này lấy cơ chế, không
copy code hay phụ thuộc runtime của các repo bên ngoài.

## Các repo đã kiểm tra

| Repo | Điều đáng học | Quyết định trong kit |
|---|---|---|
| [OpenViking](https://github.com/volcengine/OpenViking) | Gom Memory/Resource/Skill vào một context tree; L0/L1/L2 progressive loading; session commit và retrieval trajectory | Thêm `context/manifest.md.template`, giữ TIER map, execution ledger và architecture snapshot; chưa kéo database/vector runtime vào core |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | Always-on ruleset, mode intensity, YAGNI ladder, root-cause caller tracing, một check runnable cho logic không tầm thường | Đưa minimality checkpoint + rule chống abstraction/dependency thừa vào contract và workflow; không ép “lazy” lên security, validation, accessibility hay yêu cầu rõ của user |
| [Superpowers](https://github.com/obra/superpowers) | Skill check trước hành động; design/spec trước code; plan bite-sized; fresh subagent + spec/quality review; ledger chống lặp sau compaction; TDD/evidence | Bổ sung `sk-execution-contract`, ledger, no-placeholder plan, per-subtask review và routing; vẫn giữ compatibility với host không có subagent |
| [Archify](https://github.com/tt-a1i/archify) | Agent skill + Node.js renderer/validator; typed JSON IR → HTML/SVG; architecture/workflow/sequence/data-flow/lifecycle; Before/Delta/After comparison | Dùng làm renderer/verification tùy chọn trong `addons/archify`; giữ JSON source, git SHA và validation receipt; không thay thế source code |

## Những gì không đưa vào core

- Không thêm OpenViking server/vector DB vì kit hiện là portable Markdown.
- Không bắt buộc một plugin/hook riêng cho từng IDE.
- Không cho Archify HTML override code/test hoặc context đã approved.
- Không biến mọi task thành multi-agent; chỉ fan-out khi task độc lập và có contract.

## Archify chi tiết

Archify là repo chính xác cho phần “vẽ kiến trúc bằng HTML”: [tt-a1i/archify](https://github.com/tt-a1i/archify).
Nó không chỉ là HTML template; agent tạo JSON IR có kiểu, Archify validate rồi
compile deterministically thành một HTML tự chứa. README chính thức mô tả các
diagram type architecture, workflow, sequence, data-flow và lifecycle; output có
thể xuất HTML, PNG, SVG, WebM và share card. Skill cũng có `validate`, `deliver`
và `compare` để đối chiếu Before/Delta/After snapshot.

Điểm quan trọng với Agent-Dev-Kit:

- Archify giúp agent và người cùng xem một artifact trực quan, dễ review.
- Typed JSON + validation receipt làm giảm việc AI tự bịa node/route.
- Snapshot có thể gắn với git SHA và source evidence.
- `compare` phù hợp với `/wf-review --deep` khi đổi kiến trúc.
- Archify là renderer/validation layer; không nên coi HTML là ground truth.

Giới hạn:

- Cần Node.js/skill cài riêng nếu muốn render thật.
- Nó không tự trở thành dependency graph engine của Agent-Dev-Kit.
- Với diagram phản ánh code thật, phải yêu cầu agent inspect source và ghi revision/evidence.

## Tiêu chí thành công sau cập nhật

- Agent biết đọc context nào ở L0/L1/L2 trước khi code.
- Có ledger để resume mà không re-run task đã hoàn tất.
- Mỗi subtask có spec review và quality review.
- Mọi “done” có command/evidence hoặc status blocker rõ.
- Các đường dẫn workflow trong README/SYSTEM tồn tại thật.
