# Thực thi agent, governance và quality gate

**Mindset:** agent phải có phạm vi rõ, ownership, reviewer/evidence và least privilege. File này không đề xuất thay control plane hiện tại bằng một runtime mới.

← [Index](../../2026-10-04-kit-secondbrain-repo-assessment.md) · [Lộ trình agent](implementation-roadmap.md)

## Pattern đáng giữ trong core

- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail): kiểm minimality, tránh abstraction/dependency thừa, giữ validation.
- [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd): output rõ kết quả trước, bước làm theo sau; chỉ là tùy chọn giao tiếp.

Các repo phục vụ việc học và xây sản phẩm của developer được phân tích trong [công cụ phát triển](../developer/development-quality.md). Ponytail ở đây vì ứng dụng chính là checkpoint hành vi của coding agent; developer cũng có thể dùng cùng checklist khi review.

## Control plane và team agent

| Repo | Điều đáng học | Quyết định |
|---|---|---|
| [paperclipai/paperclip](https://github.com/paperclipai/paperclip) | Atomic task checkout, task thread bền vững, heartbeat, review/approval, budget, skills/evals versioned. | Học task ownership, run history và review gate. Không đưa full control plane vào core. |
| [mvschwarz/openrig](https://github.com/mvschwarz/openrig) | Team YAML, owner/checker, shared context, owned work và queue bền vững. | Học cho `addons/swarm`; chưa PoC local vì native Windows không hỗ trợ và setup ghi hooks/trust. |
| [NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell) | Policy file/process/network, credential chỉ ở endpoint được phép, đánh giá thay đổi policy. | Học least privilege/approval. Chỉ xem runtime khi agent chạy nền cần sandbox hạ tầng. |

## Nguyên tắc áp dụng vào Kit

1. Một task có owner và completion evidence rõ ràng.
2. Reviewer kiểm exact candidate, không chỉ tóm tắt của agent thực thi.
3. Budget, permission và external action là policy rõ ràng, không suy từ prompt.
4. Runtime mới chỉ là addon sau khi baseline workflow/ledger hiện có bộc lộ khoảng trống đo được.

**PoC team agent:** một thay đổi nhỏ trong repo, hai vai trò owner/checker, task ID, evidence test/diff và một quyết định có người chịu trách nhiệm. Đo can thiệp thủ công, chi phí, khả năng tiếp tục và lỗi phối hợp.
