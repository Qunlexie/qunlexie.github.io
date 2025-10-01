# Personal Website & Notes Hub

This repository contains my personal website hosted on GitHub Pages, featuring a comprehensive **free and open** notes system for study materials.

## 🌟 Free & Open Knowledge

**Knowledge is free!** This notes system has no passwords, no authentication, no paywalls - just pure learning. Anyone can access, use, and learn from these materials freely.

## 📚 Notes Hub System

### Features
- **Completely Free Access**: No passwords or authentication required
- **Multi-folder Support**: Organize notes by subject (algorithms, mltheory, etc.)
- **Mobile-friendly**: Optimized for mobile revision
- **Auto-discovery**: Build system automatically finds and processes all note folders
- **Open Source**: All notes are freely accessible to everyone

## 📚 Notes Hub System

### Quick Start:
```bash
# Add your notes
echo "# My Notes" > notes/my-subject/topic.md

# Build and preview
python3 src/build_notes.py
open pages/notes.html

# Deploy
git add *.html
git commit -m "Update notes"
git push
```

### File Structure:
```
├── pages/notes.html           # Main notes hub (freely accessible)
├── notes-html/                # Auto-generated topic pages
│   ├── domains-cv.html
│   ├── domains-nlp.html
│   └── ...
├── notes/                     # Source markdown files
│   ├── mltheory/
│   │   └── dltheory.md        # ML Theory notes
│   ├── domains/
│   │   └── cv.md              # Computer Vision notes
│   └── [any-folder]/          # Add any topic folder
├── src/build_notes.py         # Multi-folder build script
└── update.sh                  # Quick update script
```

### Multi-Folder System:
- **Automatic Discovery:** Build script scans `notes/` folder
- **Dynamic Generation:** Creates HTML pages for all `.md` files
- **Scalable Structure:** Add any folder/topic without code changes
- **Consistent Navigation:** All pages use same styling and structure
- **Smart Naming:** Files named as `folder-topic.html`
- **Free Access:** No authentication required - knowledge is free!

### Adding New Topics:
1. Create folder: `mkdir notes/new-topic`
2. Add markdown: `notes/new-topic/my-notes.md`
3. Run build: `python3 src/build_notes.py`
4. Access via: `qunlexie.github.io/notes-html/new-topic-my-notes.html`

### Workflow:
1. **Edit notes** in `notes/[subject]/[topic].md` (simple markdown)
2. **Build** with `python3 src/build_notes.py`
3. **Preview** the notes hub at `pages/notes.html`
4. **Commit** all generated HTML files
5. **Access** freely via `qunlexie.github.io/pages/notes.html` - no password needed!

## 🚀 Deployment

Simple manual deployment via GitHub Pages - just push to main branch.

📖 **See [DEPLOYMENT.md](DEPLOYMENT.md) for simple setup instructions**

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

**Knowledge is free!** 🌟

## 📱 Mobile Access

The notes page is fully responsive and works great on mobile devices for quick revision.

---

**Note:** This system makes all notes freely accessible to everyone - knowledge is free!

