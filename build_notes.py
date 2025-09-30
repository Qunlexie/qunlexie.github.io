#!/usr/bin/env python3
"""
Build script to convert markdown notes to HTML format.
Reads from notes/ folder (gitignored) and updates ml-theory.html
"""

import re
from pathlib import Path

def parse_markdown_to_html(md_file):
    """Convert markdown file to HTML content"""
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    html_content = []
    in_list = False
    in_nested_list = False
    in_deep_nested_list = False
    
    for line in lines:
        original_line = line
        line = line.rstrip()
        
        # Skip empty lines
        if not line.strip():
            continue
            
        # Skip the title line
        if line.strip().startswith('ML Theory'):
            continue
        
        # Count leading spaces
        leading_spaces = len(original_line) - len(original_line.lstrip())
        content = line.strip()
        
        # Skip if not a bullet point
        if not content.startswith('- '):
            continue
        
        # Remove the '- ' prefix
        content = content[2:].strip()
        
        # Top-level (0 spaces) - Questions
        if leading_spaces == 0:
            # Close any open nested lists
            if in_deep_nested_list:
                html_content.append('                    </ul>')
                in_deep_nested_list = False
            if in_nested_list:
                html_content.append('                </ul>')
                in_nested_list = False
            if in_list:
                html_content.append('            </ul>')
                in_list = False
            
            # Add question
            html_content.append(f'            <p><strong>{content}</strong></p>')
            
        # First level indent (4 spaces) - Top-level answers
        elif leading_spaces == 4:
            # Close nested lists if open
            if in_deep_nested_list:
                html_content.append('                    </ul>')
                in_deep_nested_list = False
            if in_nested_list:
                html_content.append('                </ul>')
                in_nested_list = False
                
            if not in_list:
                html_content.append('            <ul style="margin-left: 1.5rem;">')
                in_list = True
            
            html_content.append(f'              <li>{content}</li>')
            
        # Second level indent (8 spaces) - Nested answers
        elif leading_spaces == 8:
            # Close deep nested if open
            if in_deep_nested_list:
                html_content.append('                    </ul>')
                in_deep_nested_list = False
                
            if not in_nested_list:
                html_content.append('                <ul style="margin-left: 1.5rem;">')
                in_nested_list = True
            
            html_content.append(f'                  <li>{content}</li>')
            
        # Third level indent (12+ spaces) - Deep nested answers
        elif leading_spaces >= 12:
            if not in_deep_nested_list:
                html_content.append('                    <ul style="margin-left: 1.5rem;">')
                in_deep_nested_list = True
            
            html_content.append(f'                      <li>{content}</li>')
    
    # Close any open lists
    if in_deep_nested_list:
        html_content.append('                    </ul>')
    if in_nested_list:
        html_content.append('                </ul>')
    if in_list:
        html_content.append('            </ul>')
    
    return '\n'.join(html_content)

def get_password():
    """Read password from local file"""
    password_file = Path('password.txt')
    if password_file.exists():
        with open(password_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Get the first non-comment line
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    return line
    print("Warning: password.txt not found or empty, using default password")
    return 'mltheory2025'

def update_html_file(html_content):
    """Update ml-theory.html with new content"""
    html_file = Path('ml-theory.html')
    password = get_password()
    
    with open(html_file, 'r', encoding='utf-8') as f:
        full_html = f.read()
    
    # Find the section to replace
    start_marker = '<!-- Your ML Theory Notes -->'
    end_marker = '</section>'
    
    start_idx = full_html.find(start_marker)
    if start_idx == -1:
        print("Error: Could not find start marker in HTML file")
        return False
    
    # Find the end of the section
    section_start = full_html.find('<section', start_idx)
    section_end = full_html.find(end_marker, section_start) + len(end_marker)
    
    # Build new section
    new_section = f'''<!-- Your ML Theory Notes -->
        <section class="category-section">
          <h2>Deep Learning Fundamentals</h2>
          <div style="line-height: 1.8;">
{html_content}
          </div>
        </section>'''
    
    # Replace the section
    updated_html = full_html[:start_idx] + new_section + full_html[section_end:]
    
    # Replace password in the HTML using regex
    import re
    password_pattern = r"const PASSWORD = '[^']*';"
    updated_html = re.sub(password_pattern, f"const PASSWORD = '{password}';", updated_html)
    
    # Write back
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    
    return True

def main():
    """Main function"""
    # Path to markdown notes
    notes_file = Path('notes/mltheory/dltheory.md')
    
    if not notes_file.exists():
        print(f"Error: Notes file not found: {notes_file}")
        return
    
    print(f"Reading notes from: {notes_file}")
    html_content = parse_markdown_to_html(notes_file)
    
    print(f"Generated {len(html_content)} characters of HTML content")
    if len(html_content) < 100:
        print("WARNING: Content seems too short!")
        print(f"Content preview: {html_content[:200]}")
    
    print("Updating ml-theory.html...")
    if update_html_file(html_content):
        print("✅ Successfully updated ml-theory.html!")
        print("Your notes are now formatted in the HTML file.")
        print("\nNext steps:")
        print("1. Open ml-theory.html in browser to preview")
        print("2. If it looks good, commit and push ml-theory.html")
        print("3. Your raw notes in notes/ folder will NOT be committed (gitignored)")
    else:
        print("❌ Failed to update HTML file")

if __name__ == '__main__':
    main()

