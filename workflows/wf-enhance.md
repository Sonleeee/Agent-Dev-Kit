---
id: enhance
type: utility
entry-command: /wf-enhance
next: review
skills-suggested:
  - core/sk-execution-contract
  - core/sk-doubt-critic
---

# /wf-enhance

**Mục tiêu:** tối ưu/refactor có chủ đích với diff nhỏ và evidence trước/sau.

## Quy trình

1. Dùng CodeGraph hoặc architecture map để xác định flow và blast radius.
2. Ghi baseline: behavior, test/build, metric hoặc code smell cần cải thiện.
3. Chạy minimality checkpoint; nếu chưa chứng minh cần đổi thì dừng.
4. Lập plan bounded rồi thực thi qua `/wf-impl`.
5. Verify regression + baseline sau thay đổi, sau đó `/wf-review`.

Với migration lớn cần kiểm soát rủi ro, dùng `/wf-delivery --deep` và ghi rõ phạm vi
kiến trúc trong execution contract.
