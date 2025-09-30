# Personal Website & Notes Hub

This repository contains my personal website hosted on GitHub Pages, featuring a comprehensive notes system for private study materials.

## 🔐 Notes System

### Features
- **Single Password Access**: One password (`notes2025`) unlocks all notes
- **Session-based Authentication**: Enter password once, access all pages seamlessly
- **Multi-folder Support**: Organize notes by subject (algorithms, mltheory, etc.)
- **Mobile-friendly**: Optimized for mobile revision
- **Private Source**: Raw markdown files are gitignored and never committed
- **Auto-discovery**: Build system automatically finds and processes all note folders

## 📚 Notes Hub System

### Quick Start:
```bash
# Add your notes
echo "# My Notes" > notes/my-subject/topic.md

# Build and preview
python3 build_notes.py
open notes.html

# Deploy
git add *.html
git commit -m "Update notes"
git push
```

### File Structure:
```
├── notes.html              # Main notes hub (password-protected)
├── *-*.html               # Auto-generated topic pages
├── notes/                  # Private notes (gitignored)
│   ├── mltheory/
│   │   └── dltheory.md     # ML Theory notes
│   ├── datascience/
│   │   └── fundamentals.md # Data Science notes
│   ├── software-engineering/
│   │   └── concepts.md     # Software Engineering notes
│   └── [any-folder]/      # Add any topic folder
├── build_notes.py          # Multi-folder build script
├── password.txt            # Your password (gitignored)
└── update.sh               # Quick update script
```

### Multi-Folder System:
- **Automatic Discovery:** Build script scans `notes/` folder
- **Dynamic Generation:** Creates HTML pages for all `.md` files
- **Scalable Structure:** Add any folder/topic without code changes
- **Consistent Navigation:** All pages use same password and styling
- **Smart Naming:** Files named as `folder-topic.html`

### Adding New Topics:
1. Create folder: `mkdir notes/new-topic`
2. Add markdown: `notes/new-topic/my-notes.md`
3. Run build: `./update.sh`
4. Access via: `qunlexie.github.io/new-topic-my-notes.html`

### Workflow:
1. **Edit notes** in `notes/[subject]/[topic].md` (simple markdown)
2. **Build** with `python3 build_notes.py`
3. **Preview** the notes hub at `notes.html`
4. **Commit** all generated HTML files
5. **Access** via `qunlexie.github.io/notes` with password `notes2025`

## 🚀 Deployment

GitHub Pages automatically deploys when you push to main branch.

## 🔑 Password Management

- **Password:** `notes2025` (stored in `password.txt` - gitignored)
- **Security:** Password file never committed to repository
- **Change password:** Edit `password.txt` → Run build script
- **Auto-injection:** Password injected into all HTML pages during build

## 📱 Mobile Access

The notes page is fully responsive and works great on mobile devices for quick revision.

---

**Note:** This system keeps your raw notes private while making formatted versions accessible via password protection.

