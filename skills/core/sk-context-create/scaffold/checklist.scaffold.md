# Checklist Scaffold

> Agent fill nội dung bên dưới dựa trên project context.
> File này bổ sung cho global checklist, KHÔNG thay thế.

---

## Global Reference

> Checklist master nằm tại `quality/checklists/` trong Core Kit.
> Mọi item dưới đây là BỔ SUNG cho global checklist.

## Project-Specific Items

### Architecture Compliance

- [ ] Code follow đúng layer responsibilities (xem `architecture.md` TIER-0 §2)
- [ ] Exception handling dùng đúng taxonomy (xem `architecture.md` TIER-0 §3)
- [ ] Naming convention đúng (xem `architecture.md` TIER-0 §4)
- [ ] Không vi phạm Known Anti-Patterns (xem `architecture.md` TIER-0 §6)

### Pattern Compliance

- [ ] Code match template trong `templates/{scope}/feature.md.template`
- [ ] Decision Questions đã trả lời trước khi code
- [ ] Không introduce pattern mới mà chưa qua review

### Project Rules

<!-- Thêm rules riêng của project tại đây -->
- [ ] {project-specific rule 1}
- [ ] {project-specific rule 2}

## Module-Specific Checklists

<!-- Nếu có module đặc biệt cần checklist riêng -->

### {Module Name} (nếu có)

- [ ] {module-specific item 1}
- [ ] {module-specific item 2}
