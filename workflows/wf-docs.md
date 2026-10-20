---
id: docs
type: utility
entry-command: /wf-docs
skills-suggested:
  - core/sk-execution-contract
  - research/sk-docs-seeker
---

> [!IMPORTANT]
> ## Delegation Policy � �?c TRU?C khi b?t d?u
>
> | �i?u ki?n | H�nh d?ng B?T BU?C |
> |:---|:---|
> | C?n scan drift tr�n = 10 docs files | **PH?I** `invoke_subagent(TypeName="research", Role="Docs Scanner")` |
> | Update = 3 docs files | Ch?y inline, KH�NG c?n subagent |


# /wf-docs

**Mục tiêu:** cập nhật documentation theo code thật, không tạo tài liệu tưởng tượng.

## Quy trình

1. Xác định audience và source of truth.
2. Scan diff/structure, tìm drift và broken links.
3. Sửa tài liệu nhỏ nhất đủ giải thích cách dùng, constraint và verify.
4. Render/preview nếu là tài liệu có layout.
5. Review link, command, version và evidence.

## Pre-completion Checklist (PH?I verify tru?c khi k?t th�c)

- [ ] �� ki?m tra Delegation Policy ? d?u file?
- [ ] Docs d?a tr�n code th?t (kh�ng tu?ng tu?ng)?
- [ ] Links v� commands verified?
