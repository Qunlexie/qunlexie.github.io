#!/bin/bash
# Enhanced update script: builds all notes with multi-folder support

echo "🔨 Building multi-folder notes system..."
python3 build_notes.py

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "🌐 Opening notes hub..."
    open notes.html
    echo ""
    echo "📚 Your multi-folder notes system:"
    echo "  • Main hub: notes.html"
    echo "  • Generated pages:"
    ls -1 *-*.html 2>/dev/null | sed 's/^/    - /'
    echo ""
    echo "Next steps:"
    echo "  git add *.html"
    echo "  git commit -m 'Update multi-folder notes system'"
    echo "  git push"
else
    echo "❌ Build failed!"
    exit 1
fi

