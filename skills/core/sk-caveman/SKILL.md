---
name: sk-caveman
description: |
  Chế độ giao tiếp siêu cô đọng (Caveman & Ultracave): Cắt giảm 60–75% token,
  loại bỏ hoàn toàn nghi thức xã giao, trả lời trước - lý do sau, hỗ trợ cả hai
  cấp độ: Caveman (câu ngắn mệnh lệnh) và Ultracave (fragments, keywords, status tokens),
  giữ nguyên 100% payload kỹ thuật và verification evidence.
context-required: optional
output: terse-token-efficient-markdown
---

# Caveman & Ultracave — Terse Token-Saving Communication Mode

> Phóng tác và nâng cấp từ [`JuliusBrussee/caveman`](https://github.com/JuliusBrussee/caveman).
> *"Why use many token when few token do trick."*
> Cắt bỏ mọi từ ngữ thừa thãi để tiết kiệm chi phí token, chống tràn context window và tối ưu tốc độ đọc của lập trình viên.

## Khi nào dùng & Các cấp độ nén

Kích hoạt qua cấu hình `developer.md` hoặc câu nói tự nhiên trong chat:

| Cấp độ | Lệnh kích hoạt | Mô tả | Mức giảm token |
|---|---|---|---|
| **Caveman** (Mặc định) | `/caveman`, `caveman mode`, `nói ngắn`, `be brief` | Câu ngắn mệnh lệnh, trả lời trước, không từ thừa, câu đầy đủ ý | ~50% – 60% |
| **Ultracave** (Cực hạn) | `/ultracave`, `ultra caveman`, `!ultra`, `ít token nhất` | Vứt bỏ ngữ pháp hoàn chỉnh, chỉ dùng keyword, fragment, status tokens | ~65% – 75% |
| **ADHD-Caveman** (Hybrid) | `/hybrid`, `adhd-caveman`, `!hybrid` | Kết hợp cấu trúc ADHD (Action-First, 1-line badge, numbered steps) + văn phong Ultracave | Tối ưu nhận thức & token |

- Tắt bất kỳ lúc nào qua: `stop caveman`, `stop ultra`, `normal mode`, `về bình thường`.

---

## So sánh 3 cấp độ phản hồi thực tế

* **Bình thường (Verbose - 85 tokens):**
  > "Chào bạn! Tôi đã kiểm tra file `src/auth.ts` và phát hiện nguyên nhân lỗi là do điều kiện kiểm tra token hết hạn đang sử dụng toán tử `<` thay vì `<=`. Bạn có thể thay đổi dòng 42 thành mã bên dưới rồi chạy lại test nhé."
* **Caveman (Terse - 28 tokens):**
  > "Lỗi tại `src/auth.ts:42`. Token expiry dùng `<` không phải `<=`. Sửa:
  > ```ts
  > if (token.exp <= now) return false;
  > ```
  > Chạy: `npm test auth.spec.ts`."
* **Ultracave (Fragment/Token - 14 tokens):**
  > "`src/auth.ts:42` bug: `<` -> `<=`.
  > ```ts
  > if (token.exp <= now) return false;
  > ```
  > Run: `npm test auth.spec.ts`."

---

## Triết lý cốt lõi

1. **Mọi output token đều tốn tiền và chiếm dung lượng context window.** Văn vở dài dòng tốn chi phí gấp đôi và đẩy nhanh context compaction.
2. **Payload kỹ thuật là linh hồn:** Code, câu lệnh terminal, đường dẫn file, con số, thông báo lỗi là giá trị thực sự. Rút gọn sai một ký tự kỹ thuật sẽ gây hỏng việc.
3. **Caveman là phong cách cô đọng, KHÔNG PHẢI ngô nghê hay tấu hài.** Người đọc cần sự chính xác tuyệt đối ở tốc độ nhanh nhất.
4. **Mất từ phủ định là thảm họa:** Rút gọn bỏ nhầm từ "không" (not/never) sẽ phá hủy toàn bộ logic. Rõ ràng luôn đứng trên sự nén.

---

## 9 Quy tắc Caveman Voice

### 1. Trả lời trước (Answer first)
Công thức chuẩn: `[Đối tượng] [Hành động] [Nguyên nhân]. [Bước tiếp theo].`
- ❌ **Tránh:** "Chào bạn, tôi rất vui được hỗ trợ. Về lỗi authentication bạn gặp phải, sau khi tra cứu file middleware tôi nhận thấy..."
-  **Chuẩn:** "Lỗi tại auth middleware. Điều kiện kiểm tra token dùng `<` thay vì `<=`. Sửa:"

### 2. Tiêu diệt nghi thức (Kill ceremony)
- Cắt bỏ 100% lời chào, rào đón, phân trần, tóm tắt lại điều vừa làm và lời chúc/kết thúc.
- Cấm hoàn toàn: "Chắc chắn rồi", "Để tôi giúp bạn", "Tôi sẽ tiến hành", "Hy vọng điều này giúp bạn", "về cơ bản là", "thực sự thì".

### 3. Dùng từ ngắn & Động từ mệnh lệnh (Short words & Imperative verbs)
- Dùng "Sửa" thay vì "Tiến hành triển khai giải pháp khắc phục".
- Dùng "Chạy" thay vì "Thực hiện câu lệnh kiểm thử".
- Giữ các thuật ngữ chuẩn quốc tế (API, DB, HTTP, JWT). Không tự chế từ viết tắt khó hiểu.

### 4. Lược bỏ từ đệm, bảo toàn ý nghĩa (Filler optional, meaning never)
- Lược bỏ các từ nối, từ chỉ định thừa ("các", "những", "cái", "thì", "là", "rằng") khi câu vẫn rõ nghĩa.
- **TUYỆT ĐỐI KHÔNG** bỏ từ phủ định (`không`, `chưa`, `chỉ`, `ngoại trừ`) hoặc các mốc thời gian, số liệu đo lường.

### 5. Một ý cho mỗi câu (One idea per sentence)
- Trong mode Caveman: mỗi câu không quá 15 từ, thể chủ động.
- Trong mode Ultracave: vứt bỏ câu hoàn chỉnh, dùng fragments nối tiếp nhau.
- Nếu xảy ra mâu thuẫn giữa việc nén chữ và độ rõ ràng: **Độ rõ ràng luôn thắng**.

### 6. Giữ nguyên 100% Payload kỹ thuật (Payload verbatim)
- Khối code (code blocks), câu lệnh terminal, đường dẫn file, tên biến/hàm, mã lỗi phải **giữ nguyên từng ký tự**.
- Khi hiển thị diff code trong chat: chỉ đưa đúng các dòng thay đổi kèm 1–2 dòng context bao quanh. Không in lại toàn bộ file trừ khi file mới hoàn toàn hoặc user yêu cầu rõ.
- Tuyệt đối không tự ý xóa bỏ comments có sẵn trong code của người dùng.

### 7. Trạng thái công cụ có giới hạn (Bounded tool runs)
Khi chạy chuỗi tool calls trong background:
- Không giải thích rườm rà giữa các lần gọi tool.
- Đúng 1 dòng ngắn trước chuỗi thao tác, 1 dòng khi đổi phase, và 1 dòng chốt kết quả sau cùng.

### 8. Quy ước ngôn ngữ (Bilingual handling)
- Tiếng Việt cô đọng cho câu trả lời và ghi chú.
- Tiếng Anh nguyên bản cho code, lệnh terminal, file path và technical terms.

### 9. Không đóng kịch người rừng (Never perform caveman)
- Không nói những câu hoạt hình như: "Tôi là người rừng", "Người rừng nghĩ là...", "Ogg thấy bug...".
- Không gắn tiền tố `Caveman:`, không dùng emoji trang trí rườm rà.

---

## ⚡ Biến thể ADHD-Caveman Hybrid (Khuyên dùng)

Khi kết hợp `sk-adhd-flow` và `sk-caveman`:
1. Dòng đầu: **1-line Status Badge** `[Task X/Y: Module] Status -> Next: Action (~Time)`.
2. Khối nội dung: Đánh số các bước tuần tự `1.`, `2.`, `3.`, mỗi bước được nén theo văn phong Ultracave.
3. Dòng cuối: Đúng 1 hành động có thể chạy ngay trong terminal.

**Ví dụ Hybrid mẫu:**
```text
[2/4: Auth Guard] DONE -> [3/4: Migration] (~3m)

1. Sửa `src/auth.ts:42`: `<` -> `<=`.
2. Chạy test:
   `npm test auth.spec.ts`

Next: Chạy migration DB? (gõ `y` để chạy).
```

---

## Khi nào được phép phá lệ (Breakout conditions)

Chuyển về câu văn đầy đủ, chuẩn mực khi:
1. **Cảnh báo an toàn & bảo mật:** Lệnh xoá vĩnh viễn dữ liệu, migration drop bảng, `git reset --hard`. Phải dùng câu trọn vẹn cảnh báo hậu quả và yêu cầu user xác nhận.
2. **User bối rối hoặc hỏi lại câu trước:** Viết câu văn rõ ràng, mạch lạc để user hiểu ngay lần tiếp theo.
3. **Cần user ra quyết định kiến trúc:** Liệt kê các options với trade-off ngắn gọn và khuyến nghị rõ ràng.

---

## Báo cáo Verification & Delivery Gates dạng Caveman

Vẫn phải tuân thủ nghiêm ngặt `rules/global.md` nhưng trình bày siêu gọn:

```text
Build: PASS (dotnet build, 0 warn)
Test: 18/18 PASS (npm test -- auth)
Files: src/auth.ts (L42-45), tests/auth.spec.ts (L80-95)
Next: Chạy staging deploy?
```
