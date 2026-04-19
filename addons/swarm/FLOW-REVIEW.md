# Flow Review

## Context

Review này dựa trên:

- Global repo `.agents/`
- Project-specific `.agents/` của `TL_BIOMASS_full`

Mục tiêu là đánh giá vì sao flow hiện tại tạo ma sát trong thực tế, đặc biệt ở bước `/impl`, và đề xuất hướng rút gọn mà vẫn giữ được sức mạnh của project context (`architecture.md`, `checklist.md`, `templates/`).

---

## Điều Đang Làm Tốt

### 1. Phân tầng global vs project là đúng

Thiết kế hiện tại tách:

- global `.agents/` = workflow logic chung, quality gates, reusable skills
- project `.agents/` = pattern thật của codebase, template thật, checklist riêng

Đây là hướng đúng. Với dự án như TL_BIOMASS, phần quyết định `/impl` code có đúng hay không nằm ở:

- `AGENTS.md`
- `context/architecture.md`
- `context/templates/be|fe/`
- `context/checklist.md`

Nói cách khác: global layer nên điều phối, còn project layer mới là source of truth cho code pattern.

### 2. Có tư duy guardrails đúng

Các rule sau là đáng giữ:

- Không implement khi chưa rõ problem/scope
- Bugfix phải root-cause first
- Phải đánh dấu API contract
- Không claim xong khi chưa có evidence

Đây là phần có giá trị lâu dài, không nên bỏ.

### 3. Project template approach của TL_BIOMASS là rất mạnh

Project này không chỉ có `architecture.md`, mà còn có template BE/FE rất cụ thể. Đây là điểm mạnh hơn hẳn kiểu chỉ dùng “reference module”.

Đặc biệt:

- BE template guide buộc AI chọn đúng template theo loại feature
- FE template guide chỉ rõ naming, request/response split, service/page pattern
- Checklist project có các pattern checks rất sát thực tế

Đây mới là thứ giúp `/impl` bám pattern.

---

## Vấn Đề Cốt Lõi

### 1. Flow global đang dài hơn nhu cầu thực tế

Flow hiện tại:

`/biz-research -> /brainstorm -> /solution -> /solution-plan -> /impl -> /preview`

Trên thực tế, nhiều task chỉ cần:

- làm rõ problem + risk
- chốt approach
- implement đúng pattern
- review

Hai cặp bước đang chồng nghĩa rõ nhất:

- `/biz-research` và `/brainstorm`
- `/solution` và `/solution-plan`

Hệ quả là user phải “điền form nhiều lần”, còn agent thì tốn context window nhưng không tăng độ đúng tương ứng.

### 2. `/impl` đang bị nhồi quá nhiều trách nhiệm

Hiện tại `/impl` vừa phải:

- đọc plan
- load context
- gọi subagent implement
- review spec
- review quality
- chạy build/test
- loop retry

Đây là nơi dễ timeout nhất, đặc biệt khi subagent là Gemini-CLI qua MCP/stdio.

### 3. Global flow đang assume nhiều hơn mức integration thực tế đảm bảo được

Tài liệu mô tả một orchestration khá lý tưởng:

- call Gemini-CLI qua MCP
- có implementer + reviewer riêng
- có status handling
- có retry loop

Nhưng repo hiện tại mới mô tả flow nhiều hơn là định nghĩa operational contract rõ ràng cho:

- timeout budget
- task chunk size
- retry strategy
- fallback khi subagent cần context thêm
- điều kiện tách task

Khi integration không ổn định, flow dài sẽ sập trước.

### 4. Global repo chưa đặt project template đúng vị trí trung tâm của `/impl`

Trong thực tế của TL_BIOMASS:

- code đúng pattern phụ thuộc mạnh vào `context/templates/`
- nhiều case không thể “nhìn module cũ rồi bắt chước”
- phải chọn đúng template theo loại task

Nhưng ở global flow hiện tại, template được xem như “tham khảo thêm”, chưa phải mandatory execution contract.

### 5. Checklist cuối đang hơi nặng

`38 items + T1-T13/T1-T14` phù hợp cho review cuối hoặc task lớn. Nếu biến nó thành thói quen mặc định cho mọi task thì agent dễ sa vào checklist theater.

Checklist nên là:

- map theo task-features ở step plan
- review subset trong đa số task
- chỉ full-scan khi task lớn hoặc trước ship

---

## Các Điểm Drift Cụ Thể Trong Repo

### 1. Tên MCP tool/server chưa nhất quán

Ví dụ đang tồn tại đồng thời:

- `mcp_geminicli_run_task`
- `mcp_gemini-swarm_gemini_run_task`
- config server name `gemini-cli`

Điểm này cần thống nhất trước khi bàn sâu hơn về orchestration.

### 2. Một số tham chiếu chéo chưa đồng bộ

`workflows/solution-plan.md` đang nhắc tới `quality/feature-bug-mapping.md`, nhưng repo hiện có:

- `quality/feature-bug-gates.md`
- `quality/mapping-rules.md`

Các drift nhỏ kiểu này làm agent khó tin cậy vào flow.

### 3. Tài liệu vẫn mô tả flow 6 bước là “main path”

Trong khi usage thực tế của bạn đang là:

- hỏi đáp/risk discovery
- chốt hướng
- `/impl`

Tức là tài liệu và hành vi thật đang lệch nhau.

---

## Đề Xuất Kiến Trúc Flow Mới

### Nguyên tắc

1. Global layer chỉ nên quyết định:
   - có cần làm rõ thêm không
   - có đủ điều kiện để code chưa
   - cần review ở mức nào

2. Project layer quyết định:
   - code pattern
   - template phải dùng
   - anti-pattern riêng
   - checklist riêng

3. `/impl` phải là bước thi hành hẹp, không phải “siêu pipeline”.

### Flow mới nên rút về 4 bước

`/clarify -> /plan -> /impl -> /review`

Trong đó:

- `/clarify`: làm rõ problem, scope, risks, open questions, root cause nếu là bug
- `/plan`: chốt approach, impacted modules, pattern constraints, template selection, test obligations
- `/impl`: implement task đã bounded, dựa trên project context và template
- `/review`: verify theo checklist subset/full tùy task

### Shortcut nên có 2 loại

- `/delivery-lite`: task rõ, đi thẳng `clarify-lite -> plan-lite -> impl -> review`
- `/delivery`: task phức tạp, cho phép hỏi đáp và plan kỹ hơn

---

## Hệ Quả Tốt Của Flow Mới

- Ít bước hơn nhưng không bỏ quality gate
- Đúng cách bạn đang làm thật
- Đẩy trọng tâm của `/impl` sang project template thay vì generic plan text
- Giảm nguy cơ timeout khi gọi Gemini-CLI
- Dễ dạy user cách dùng hơn

---

## Khuyến Nghị Thực Thi

### Nên làm ngay

- Thêm workflow V2 song song với flow cũ
- Định nghĩa `/clarify`, `/plan`, `/delivery-lite`
- Ghi rõ project templates là mandatory input của `/impl`
- Giới hạn `/impl` chỉ nhận task đã bounded

### Nên làm tiếp theo

- Chuẩn hóa naming cho MCP server/tool
- Tách policy timeout/retry cho Gemini-CLI ra tài liệu riêng
- Đổi `/preview` thành `/review`, giữ alias cũ để tương thích

### Không nên làm

- Không nên thêm thêm bước mới vào flow cũ
- Không nên cố ép mọi task đi đủ 6 bước
- Không nên kỳ vọng agent đọc `architecture.md` là tự đúng pattern nếu không đọc template thực tế

---

## Kết Luận

Repo này có nền tốt, nhưng đang thiên về “workflow completeness” hơn “execution ergonomics”.

Hướng đúng không phải là thêm rule, mà là:

- rút bớt stage
- đưa project templates lên trung tâm của `/impl`
- giảm orchestration giả định
- dùng flow theo đúng hành vi làm việc thực tế của bạn
