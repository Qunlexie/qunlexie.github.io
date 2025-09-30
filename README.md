# Personal Website & Private Notes System

This repository hosts my personal website with a secure private notes system for ML theory revision.

## 🔐 Security Features

- **Password-protected notes** - Access via `ml-theory.html`
- **Private source files** - Raw notes in `notes/` folder (gitignored)
- **Secure password handling** - Password stored locally, not in repository
- **Clean separation** - Public website + private notes system

## 📝 ML Theory Notes System

### Quick Start:
```bash
# Edit your notes
vim notes/mltheory/dltheory.md

# Build and preview
./update.sh

# Deploy
git add ml-theory.html
git commit -m "Update ML notes"
git push
```

### File Structure:
```
├── ml-theory.html          # Public password-protected page
├── notes/                  # Private notes (gitignored)
│   └── mltheory/
│       └── dltheory.md     # Your raw markdown notes
├── build_notes.py          # Build script
├── password.txt            # Your password (gitignored)
└── update.sh               # Quick update script
```

### Workflow:
1. **Edit notes** in `notes/mltheory/dltheory.md` (simple markdown)
2. **Build** with `python3 build_notes.py` or `./update.sh`
3. **Preview** the generated HTML
4. **Commit** only `ml-theory.html` to GitHub
5. **Access** via website with password

## 🚀 Deployment

GitHub Pages automatically deploys when you push to main branch.

## 🔑 Password Management

- Password stored in `password.txt` (gitignored)
- Change password: Edit `password.txt` → Run build script
- Password is injected into HTML during build process

## 📱 Mobile Access

The notes page is fully responsive and works great on mobile devices for quick revision.

---

**Note:** This system keeps your raw notes private while making formatted versions accessible via password protection.

