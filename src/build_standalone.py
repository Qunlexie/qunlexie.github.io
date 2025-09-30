#!/usr/bin/env python3
"""
Standalone build script with minimal dependencies.
Creates all necessary files if they don't exist.
"""

import re
import os
from pathlib import Path

def create_default_password_file():
    """Create password.txt with default password if it doesn't exist"""
    script_dir = Path(__file__).parent
    password_file = script_dir / 'password.txt'
    
    if not password_file.exists():
        print("Creating default password file...")
        with open(password_file, 'w', encoding='utf-8') as f:
            f.write("notes2025\n")
    
    return password_file

def create_notes_template():
    """Create a basic notes template if it doesn't exist"""
    notes_template = Path(__file__).parent / '../pages/notes.html'
    
    if not notes_template.exists():
        print("Creating notes template...")
        template_content = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notes Hub - Private Study Materials</title>
    <link rel="stylesheet" href="../assets/style.css" />
    <style>
      .notes-content { display: none; }
      .login-form { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 60vh; text-align: center; }
      .login-form h2 { margin-bottom: 2rem; color: #333; }
      .password-input { padding: 12px 20px; font-size: 16px; border: 2px solid #ddd; border-radius: 8px; width: 300px; max-width: 100%; margin-bottom: 1rem; }
      .password-input:focus { outline: none; }
      .login-btn { background: #007bff; color: white; border: none; padding: 12px 30px; font-size: 16px; border-radius: 8px; cursor: pointer; transition: background 0.3s; }
      .login-btn:hover { background: #0056b3; }
      .error-message { color: #dc3545; margin-top: 1rem; display: none; }
      .subject-section { margin-bottom: 3rem; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
      .subject-section h2 { color: #007bff; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid #007bff; }
      .topic-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
      .topic-card { background: #f8f9fa; padding: 1.5rem; border-radius: 8px; border: 1px solid #e9ecef; transition: all 0.3s ease; }
      .topic-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); border-color: #007bff; }
      .topic-card h3 { margin: 0 0 0.5rem 0; color: #333; }
      .topic-card h3 a { color: #007bff; text-decoration: none; font-weight: 600; }
      .topic-card h3 a:hover { text-decoration: underline; }
      .topic-card p { color: #666; margin: 0; font-size: 0.9rem; line-height: 1.4; }
      @media (max-width: 768px) { .topic-grid { grid-template-columns: 1fr; } .password-input { width: 100%; max-width: 300px; } }
    </style>
  </head>
  <body>
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
      <div class="login-form" id="loginForm">
        <h2>🔐 Private Notes Access</h2>
        <p>Enter password to access study materials</p>
        <input type="password" id="passwordInput" class="password-input" placeholder="Enter password" />
        <button onclick="checkPassword()" class="login-btn">Access Notes</button>
        <div id="errorMessage" class="error-message">Invalid password. Please try again.</div>
      </div>

      <div class="notes-content" id="notesContent">
        <h1>📚 Notes Hub</h1>
        <p>Your comprehensive collection of study materials and technical notes.</p>
        <!-- Dynamic Content Start -->
        <!-- Future Sections -->
      </div>
    </main>
    
    <footer>
      <p>&copy; 2025 Private Notes Hub</p>
    </footer>

    <script>
      const PASSWORD = 'REPLACE_WITH_ACTUAL_PASSWORD';
      function checkPassword() {
        const input = document.getElementById('passwordInput').value;
        if (input === PASSWORD) {
          document.getElementById('loginForm').style.display = 'none';
          document.getElementById('notesContent').style.display = 'block';
          sessionStorage.setItem('notesAuthenticated', 'true');
        } else {
          document.getElementById('errorMessage').style.display = 'block';
          document.getElementById('passwordInput').value = '';
        }
      }
      function checkAuth() {
        const isAuthenticated = sessionStorage.getItem('notesAuthenticated') === 'true';
        if (isAuthenticated) {
          document.getElementById('loginForm').style.display = 'none';
          document.getElementById('notesContent').style.display = 'block';
        }
      }
      document.getElementById('passwordInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') { checkPassword(); }
      });
      document.addEventListener('DOMContentLoaded', function() { checkAuth(); });
    </script>
  </body>
</html>'''
        
        # Ensure parent directory exists
        notes_template.parent.mkdir(parents=True, exist_ok=True)
        
        with open(notes_template, 'w', encoding='utf-8') as f:
            f.write(template_content)

def create_sample_notes():
    """Create sample notes if notes directory is empty"""
    script_dir = Path(__file__).parent
    notes_dir = script_dir / '../notes'
    
    if not notes_dir.exists():
        print("Creating sample notes directory...")
        notes_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a sample note
        sample_note = notes_dir / 'sample' / 'getting-started.md'
        sample_note.parent.mkdir(parents=True, exist_ok=True)
        
        with open(sample_note, 'w', encoding='utf-8') as f:
            f.write('''# Getting Started

- Welcome to your notes system
    - This is a sample note to get you started
    - You can add your own markdown files in the notes/ directory
    - The build system will automatically generate HTML pages
- Next steps
    - Create your own folders under notes/
    - Add .md files with your content
    - Run the build script to generate HTML
    - Your notes will be password-protected and ready to deploy
''')

def get_password():
    """Get password with fallback creation"""
    script_dir = Path(__file__).parent
    password_file = create_default_password_file()
    
    with open(password_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                return line
    return 'notes2025'  # Ultimate fallback

def parse_markdown_to_html(md_file):
    """Convert markdown file to HTML content with table of contents"""
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    html_content = []
    toc_items = []
    in_list = False
    in_nested_list = False
    in_deep_nested_list = False
    
    # First pass: collect all questions for TOC
    question_counter = 0
    for line in lines:
        line = line.rstrip()
        if not line.strip():
            continue
            
        # Questions (no leading spaces, starts with -)
        if line.startswith('- ') and not line.startswith('-   '):
            content = line[2:].strip()
            if content and not content.startswith('-'):
                question_counter += 1
                safe_content = re.sub(r'[^a-zA-Z0-9\s]', '', content).replace(' ', '-').lower()
                anchor_id = f"q-{safe_content[:30]}"
                toc_items.append({
                    'title': content,
                    'anchor': anchor_id,
                    'number': question_counter
                })
    
    # Generate Table of Contents
    if toc_items:
        html_content.append('            <div class="table-of-contents">')
        html_content.append('              <h3>📋 Table of Contents</h3>')
        html_content.append('              <ul class="toc-list">')
        for item in toc_items:
            html_content.append(f'                <li><a href="#{item["anchor"]}">{item["number"]}. {item["title"]}</a></li>')
        html_content.append('              </ul>')
        html_content.append('            </div>')
        html_content.append('')
    
    # Second pass: generate content (same logic as original)
    question_counter = 0
    for line in lines:
        original_line = line
        line = line.rstrip()
        
        if not line.strip():
            continue
            
        if line.strip().startswith('#'):
            continue
        
        leading_spaces = len(original_line) - len(original_line.lstrip())
        content = line.strip()
        
        if not content.startswith('- '):
            continue
        
        content = content[2:].strip()
        
        if leading_spaces == 0:
            if in_deep_nested_list:
                html_content.append('                    </ul>')
                in_deep_nested_list = False
            if in_nested_list:
                html_content.append('                </ul>')
                in_nested_list = False
            if in_list:
                html_content.append('            </ul>')
                in_list = False
            
            question_counter += 1
            safe_content = re.sub(r'[^a-zA-Z0-9\s]', '', content).replace(' ', '-').lower()
            anchor_id = f"q-{safe_content[:30]}"
            
            html_content.append(f'            <p id="{anchor_id}" class="question"><strong>{content}</strong></p>')
            
        elif leading_spaces == 4:
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
            
        elif leading_spaces == 8:
            if in_deep_nested_list:
                html_content.append('                    </ul>')
                in_deep_nested_list = False
                
            if not in_nested_list:
                html_content.append('                <ul style="margin-left: 1.5rem;">')
                in_nested_list = True
            
            html_content.append(f'                  <li>{content}</li>')
            
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

def discover_note_folders():
    """Discover all note folders and their markdown files"""
    script_dir = Path(__file__).parent
    notes_dir = script_dir / '../notes'
    
    # Create sample notes if directory doesn't exist
    if not notes_dir.exists():
        create_sample_notes()
    
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
            elif first_line:
                return first_line
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
    <link rel="stylesheet" href="../assets/style.css" />
    <style>
      .notes-content {{ display: block; }}
      .notes-header {{ text-align: center; margin: 2rem 0; }}
      .notes-header h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
      .notes-header .subtitle {{ color: #666; font-style: italic; }}
      .category-section {{ background: white; padding: 1.5rem; margin-bottom: 2rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
      .category-section h2 {{ font-size: 1.5rem; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid #007bff; }}
      .back-link {{ display: inline-block; margin-bottom: 1rem; color: #007bff; text-decoration: none; font-weight: 500; }}
      .back-link:hover {{ text-decoration: underline; }}
      .table-of-contents {{ background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; }}
      .table-of-contents h3 {{ margin-top: 0; margin-bottom: 1rem; color: #495057; font-size: 1.2rem; }}
      .toc-list {{ list-style: none; padding-left: 0; margin: 0; }}
      .toc-list li {{ margin-bottom: 0.5rem; }}
      .toc-list a {{ color: #007bff; text-decoration: none; font-weight: 500; display: block; padding: 0.25rem 0; border-radius: 4px; transition: all 0.2s ease; }}
      .toc-list a:hover {{ background-color: #e7f3ff; padding-left: 0.5rem; text-decoration: none; }}
      .question {{ margin-top: 2rem; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #e9ecef; }}
      .back-to-top {{ position: fixed; bottom: 30px; right: 30px; background: #007bff; color: white; border: none; border-radius: 50%; width: 50px; height: 50px; font-size: 18px; cursor: pointer; box-shadow: 0 4px 12px rgba(0,123,255,0.3); transition: all 0.3s ease; opacity: 0; visibility: hidden; z-index: 1000; }}
      .back-to-top:hover {{ background: #0056b3; transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,123,255,0.4); }}
      .back-to-top.visible {{ opacity: 1; visibility: visible; }}
      .back-to-top .icon {{ display: inline-block; transform: rotate(-90deg); }}
      @media (max-width: 768px) {{ .notes-header h1 {{ font-size: 2rem; }} .table-of-contents {{ padding: 1rem; }} .back-to-top {{ bottom: 20px; right: 20px; width: 45px; height: 45px; font-size: 16px; }} }}
    </style>
  </head>
  <body>
    <div class="notes-content" id="notesContent">
      <header>
        <nav>
          <ul>
            <li><a href="../pages/index.html">Home</a></li>
            <li><a href="../pages/projects.html">Projects and Research</a></li>
            <li><a href="../pages/highlights.html">Highlights</a></li>
            <li><a href="../pages/notes.html">Notes Hub</a></li>
          </ul>
        </nav>
      </header>
      
      <main>
        <div class="notes-header">
          <h1>{title}</h1>
          <p class="subtitle">comprehensive revision notes</p>
        </div>

        <div class="category-section">
          <a href="../pages/notes.html" class="back-link">← Back to Notes Hub</a>
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

    <button class="back-to-top" id="backToTop" onclick="scrollToTop()" title="Back to Table of Contents">
      <span class="icon">→</span>
    </button>

    <script>
      function checkAuth() {{
        const isAuthenticated = sessionStorage.getItem('notesAuthenticated') === 'true';
        if (isAuthenticated) {{
          document.getElementById('notesContent').style.display = 'block';
        }} else {{
          window.location.href = '../pages/notes.html';
        }}
      }}

      function scrollToTop() {{
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
      }}

      function toggleBackToTopButton() {{
        const backToTopButton = document.getElementById('backToTop');
        if (window.pageYOffset > 300) {{
          backToTopButton.classList.add('visible');
        }} else {{
          backToTopButton.classList.remove('visible');
        }}
      }}

      document.addEventListener('DOMContentLoaded', function() {{
        checkAuth();
        window.addEventListener('scroll', toggleBackToTopButton);
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
            html_file = f"../notes-html/{folder_name}-{file_name}.html"
            
            hub_content.append(f'''
            <div class="topic-card">
              <h3><a href="{html_file}">{file_title}</a></h3>
              <p>Complete reference for {file_title.lower()}</p>
            </div>''')
        
        hub_content.append('''
          </div>
        </section>''')
    
    # Create or update the hub template
    script_dir = Path(__file__).parent
    create_notes_template()  # Ensure template exists
    hub_file = script_dir / '../pages/notes.html'
    
    with open(hub_file, 'r', encoding='utf-8') as f:
        hub_html = f.read()
    
    # Replace the password first
    password_pattern = r"const PASSWORD = '[^']*';"
    hub_html = re.sub(password_pattern, f"const PASSWORD = '{password}';", hub_html)
    
    # Replace the dynamic content section
    start_marker = '<!-- Dynamic Content Start -->'
    end_marker = '<!-- Future Sections -->'
    
    start_idx = hub_html.find(start_marker)
    end_idx = hub_html.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        new_content = ''.join(hub_content)
        updated_hub = hub_html[:start_idx] + new_content + hub_html[end_idx:]
    else:
        updated_hub = hub_html
    
    # Write back
    with open(hub_file, 'w', encoding='utf-8') as f:
        f.write(updated_hub)
    
    return True

def main():
    """Main function"""
    print("🔍 Discovering note folders...")
    note_structure = discover_note_folders()
    
    if not note_structure:
        print("No note folders found. Creating sample structure...")
        create_sample_notes()
        note_structure = discover_note_folders()
    
    print(f"Found {len(note_structure)} note folders:")
    for folder, files in note_structure.items():
        print(f"  📁 {folder}: {len(files)} files")
    
    # Ensure output directory exists
    script_dir = Path(__file__).parent
    output_dir = script_dir / '../notes-html'
    output_dir.mkdir(exist_ok=True)
    
    password = get_password()
    generated_files = []
    
    # Process each folder
    for folder_name, files in note_structure.items():
        print(f"\n📚 Processing {folder_name}...")
        
        for file_info in files:
            md_file = file_info['file']
            file_title = file_info['title']
            file_name = file_info['name']
            html_file = output_dir / f"{folder_name}-{file_name}.html"
            
            print(f"  📄 {file_title} -> {html_file}")
            
            # Check if markdown file has enough content
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            if len(md_content.strip()) < 10:
                print(f"    ⚠️  Warning: {file_title} seems too short!")
                continue
            
            # Parse markdown to HTML
            html_content = parse_markdown_to_html(md_file)
            
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
    print(f"1. Open pages/notes.html in browser to preview")
    print(f"2. If it looks good, commit all HTML files")
    print(f"3. Your raw notes in notes/ folder will NOT be committed (gitignored)")

if __name__ == '__main__':
    main()
