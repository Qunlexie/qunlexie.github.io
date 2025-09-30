#!/usr/bin/env python3
"""
Enhanced build script for multi-folder notes system with automatic discovery.
Scans notes/ folder structure and generates HTML pages for all topics.
"""

import re
import os
from pathlib import Path

def parse_markdown_to_html(md_file):
    """Convert markdown file to HTML content with hyperlinks"""
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    html_content = []
    in_list = False
    in_nested_list = False
    in_deep_nested_list = False
    
    # Create anchor links for questions
    question_counter = 0
    
    for line in lines:
        original_line = line
        line = line.rstrip()
        
        # Skip empty lines
        if not line.strip():
            continue
            
        # Skip title lines (lines starting with #)
        if line.strip().startswith('#'):
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
            
            # Create anchor for question
            question_counter += 1
            safe_content = re.sub(r'[^a-zA-Z0-9\s]', '', content).replace(' ', '-').lower()
            anchor_id = f"q-{safe_content[:30]}"
            
            # Add question with anchor
            html_content.append(f'            <p id="{anchor_id}"><strong>{content}</strong> <a href="#{anchor_id}" style="color: #666; text-decoration: none;">🔗</a></p>')
            
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
    return 'notes2025'

def discover_note_folders():
    """Discover all note folders and their markdown files"""
    notes_dir = Path('notes')
    if not notes_dir.exists():
        return {}
    
    note_structure = {}
    
    for item in notes_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            folder_name = item.name
            note_structure[folder_name] = []
            
            # Find all markdown files in this folder
            for md_file in item.glob('*.md'):
                note_structure[folder_name].append({
                    'file': md_file,
                    'name': md_file.stem,
                    'title': get_file_title(md_file)
                })
    
    return note_structure

def get_file_title(md_file):
    """Extract title from markdown file"""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line.startswith('#'):
                return first_line[1:].strip()
            else:
                return md_file.stem.replace('-', ' ').replace('_', ' ').title()
    except:
        return md_file.stem.replace('-', ' ').replace('_', ' ').title()

def create_html_template(title, content, password):
    """Create HTML template for a notes page"""
    return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Notes</title>
    <link rel="stylesheet" href="style.css" />
    <style>
      /* Additional styles for notes page */
      .notes-content {{
        display: block;
      }}
      
      /* aman.ai inspired styles */
      .notes-header {{
        text-align: center;
        margin: 2rem 0;
      }}
      
      .notes-header h1 {{
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
      }}
      
      .notes-header .subtitle {{
        color: #666;
        font-style: italic;
      }}
      
      .category-section {{
        background: white;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      }}
      
      .category-section h2 {{
        font-size: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #007bff;
      }}
      
      .back-link {{
        display: inline-block;
        margin-bottom: 1rem;
        color: #007bff;
        text-decoration: none;
        font-weight: 500;
      }}
      
      .back-link:hover {{
        text-decoration: underline;
      }}
      
      @media (max-width: 768px) {{
        .notes-header h1 {{
          font-size: 2rem;
        }}
      }}
    </style>
  </head>
  <body>
    <!-- Notes Content -->
    <div class="notes-content" id="notesContent">
      <header>
        <nav>
          <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="projects.html">Projects and Research</a></li>
            <li><a href="highlights.html">Highlights</a></li>
            <li><a href="notes.html">Notes Hub</a></li>
          </ul>
        </nav>
      </header>
      
      <main>
        <div class="notes-header">
          <h1>{title}</h1>
          <p class="subtitle">comprehensive revision notes</p>
        </div>

        <div class="category-section">
          <a href="notes.html" class="back-link">← Back to Notes Hub</a>
          <h2>{title}</h2>
          <div style="line-height: 1.8;">
{content}
          </div>
        </div>

      </main>
      
      <footer>
        <p>&copy; 2025 {title} Notes</p>
      </footer>
    </div>

    <script>
      // Check if user is already authenticated
      function checkAuth() {{
        const isAuthenticated = sessionStorage.getItem('notesAuthenticated') === 'true';
        if (isAuthenticated) {{
          document.getElementById('notesContent').style.display = 'block';
        }} else {{
          // Redirect to main hub for authentication
          window.location.href = 'notes.html';
        }}
      }}

      // Initialize page
      document.addEventListener('DOMContentLoaded', function() {{
        checkAuth();
      }});
    </script>
  </body>
</html>'''

def build_notes_hub(note_structure):
    """Build the main notes hub page with dynamic content"""
    password = get_password()
    
    # Generate hub content
    hub_content = []
    
    for folder_name, files in note_structure.items():
        folder_title = folder_name.replace('-', ' ').replace('_', ' ').title()
        hub_content.append(f'''
        <section class="subject-section" id="{folder_name}">
          <h2>📚 {folder_title}</h2>
          <p>Comprehensive notes on {folder_title.lower()} topics.</p>
          
          <div class="topic-grid">''')
        
        for file_info in files:
            file_title = file_info['title']
            file_name = file_info['name']
            html_file = f"{folder_name}-{file_name}.html"
            
            hub_content.append(f'''
            <div class="topic-card">
              <h3><a href="{html_file}">{file_title}</a></h3>
              <p>Complete reference for {file_title.lower()}</p>
            </div>''')
        
        hub_content.append('''
          </div>
        </section>''')
    
    # Read the hub template
    hub_file = Path('notes.html')
    if not hub_file.exists():
        print("Error: notes.html template not found")
        return False
    
    with open(hub_file, 'r', encoding='utf-8') as f:
        hub_html = f.read()
    
    # Replace the dynamic content section
    start_marker = '<!-- ML Theory Section -->'
    end_marker = '<!-- Future Sections -->'
    
    start_idx = hub_html.find(start_marker)
    end_idx = hub_html.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        new_content = ''.join(hub_content)
        updated_hub = hub_html[:start_idx] + new_content + hub_html[end_idx:]
    else:
        # Fallback: replace password only
        password_pattern = r"const PASSWORD = '[^']*';"
        updated_hub = re.sub(password_pattern, f"const PASSWORD = '{password}';", hub_html)
    
    # Write back
    with open(hub_file, 'w', encoding='utf-8') as f:
        f.write(updated_hub)
    
    return True

def main():
    """Main function"""
    print("🔍 Discovering note folders...")
    note_structure = discover_note_folders()
    
    if not note_structure:
        print("No note folders found in notes/ directory")
        return
    
    print(f"Found {len(note_structure)} note folders:")
    for folder, files in note_structure.items():
        print(f"  📁 {folder}: {len(files)} files")
    
    password = get_password()
    generated_files = []
    
    # Process each folder
    for folder_name, files in note_structure.items():
        print(f"\n📚 Processing {folder_name}...")
        
        for file_info in files:
            md_file = file_info['file']
            file_title = file_info['title']
            file_name = file_info['name']
            html_file = f"{folder_name}-{file_name}.html"
            
            print(f"  📄 {file_title} -> {html_file}")
            
            # Parse markdown to HTML
            html_content = parse_markdown_to_html(md_file)
            
            if len(html_content) < 100:
                print(f"    ⚠️  Warning: {file_title} seems too short!")
                continue
            
            # Create HTML file
            html_template = create_html_template(file_title, html_content, password)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_template)
            
            generated_files.append(html_file)
            print(f"    ✅ Generated {len(html_content)} characters")
    
    # Build notes hub
    print(f"\n🏠 Building notes hub...")
    if build_notes_hub(note_structure):
        print("✅ Successfully updated notes hub!")
    else:
        print("❌ Failed to update notes hub")
        return
    
    print(f"\n🎉 Build complete!")
    print(f"Generated {len(generated_files)} HTML files:")
    for file in generated_files:
        print(f"  📄 {file}")
    print(f"  🏠 notes.html (hub)")
    
    print(f"\nNext steps:")
    print(f"1. Open notes.html in browser to preview")
    print(f"2. If it looks good, commit all HTML files")
    print(f"3. Your raw notes in notes/ folder will NOT be committed (gitignored)")

if __name__ == '__main__':
    main()