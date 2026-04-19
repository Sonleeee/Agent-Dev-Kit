# 📓 Obsidian Addon — Second Brain

> Tích hợp Obsidian vault làm "bộ não thứ 2" cho agent —
> tri thức xuyên projects, xuyên sessions.

## Tầm nhìn

```
Obsidian Vault (Global Brain)
├── brain/
│   ├── north-star.md          ← Goals & Direction cá nhân
│   ├── decisions/             ← ADRs xuyên projects
│   ├── knowledge/             ← Technical knowledge base
│   │   ├── dotnet/
│   │   ├── react/
│   │   └── devops/
│   ├── projects/              ← Link tới từng project
│   │   ├── [project-a]/
│   │   └── [project-b]/
│   └── daily/                 ← Daily notes, standup logs
│
│   🔗 Wikilinks kết nối xuyên suốt
│   📊 Graph View: Nhìn toàn bộ mạng lưới tri thức
```

## Setup

### 1. Cài Obsidian

- Download từ [obsidian.md](https://obsidian.md/) (free, local-first)
- Cài trên PC/Mac

### 2. Tạo Vault

```bash
mkdir -p C:\Sonlee\SecondBrain\brain\decisions
mkdir -p C:\Sonlee\SecondBrain\brain\knowledge
mkdir -p C:\Sonlee\SecondBrain\brain\projects
```

Hoặc copy từ `vault-template/` trong addon này.

### 3. Mở Vault trong Obsidian

- Obsidian → Open folder as vault → chọn `C:\Sonlee\SecondBrain\`

### 4. Kết nối với projects

- Tạo `brain/projects/[tên-project]/` cho mỗi project
- Link tới `.agents/context/architecture.md` của project
- Link tới `GRAPH_REPORT.md` nếu dùng Graphify addon

## Vault Template

Xem `vault-template/` để lấy cấu trúc starter.

## Ngôn ngữ

Viết bằng **tiếng Việt** (hoặc tùy cá nhân).
