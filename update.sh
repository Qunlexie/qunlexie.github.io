#!/bin/bash
# Quick update script: builds notes and opens preview

echo "🔨 Building notes..."
python3 build_notes.py

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "🌐 Opening preview..."
    open ml-theory.html
    echo ""
    echo "Next steps:"
    echo "  git add ml-theory.html"
    echo "  git commit -m 'Update notes'"
    echo "  git push"
else
    echo "❌ Build failed!"
    exit 1
fi

