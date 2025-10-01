# 🚀 Simple Deployment Guide - qunlexie.github.io

## Quick Deploy

This repository is set up for simple manual deployment via GitHub Pages. Here's how to get it running:

### 1. Fork or Clone
```bash
git clone https://github.com/qunlexie/qunlexie.github.io.git
cd qunlexie.github.io
```

### 2. Add Your Notes
```bash
# Create a new topic folder
mkdir notes/my-topic

# Add your notes
echo "# My Topic Notes" > notes/my-topic/intro.md
```

### 3. Build and Preview
```bash
# Generate HTML files
python3 src/build_notes.py

# Preview locally
open pages/notes.html
```

### 4. Deploy Manually
```bash
# Add all changes
git add .

# Commit changes
git commit -m "Update notes"

# Push to GitHub
git push origin main
```

GitHub Pages will automatically deploy your site to `https://yourusername.github.io`

## 🌟 Free & Open

**Knowledge is free!** This system has:
- ✅ No passwords or authentication
- ✅ No paywalls or restrictions  
- ✅ Completely open source
- ✅ Free for everyone to use and modify
- ✅ No complex deployment workflows needed

## 📚 Adding Content

### New Topics
1. Create folder: `mkdir notes/new-subject`
2. Add markdown: `notes/new-subject/topic.md`
3. Run build: `python3 src/build_notes.py`
4. Access via: `yourusername.github.io/notes-html/new-subject-topic.html`

### Markdown Format
Use simple markdown with bullet points:
```markdown
# Topic Title

- Main question or concept
  - First answer point
  - Second answer point
    - Nested detail
    - Another nested detail
- Another main question
  - Answer to second question
```

## 🔧 Customization

### Styling
- Edit `assets/style.css` for global styles
- Individual page styles are in `src/build_notes.py`

### Structure
- All notes go in `notes/` folder
- Generated HTML goes in `notes-html/` folder
- Main hub is `pages/notes.html`

## 📱 Mobile Friendly

The site is fully responsive and works great on:
- 📱 Mobile phones
- 📱 Tablets  
- 💻 Desktop computers

## 🤝 Contributing

1. Fork the repository
2. Add your notes or improvements
3. Submit a pull request
4. Help others learn!

---

**Remember: Knowledge is free! Share it freely! 🌟**