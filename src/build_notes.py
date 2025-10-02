#!/usr/bin/env python3
"""
Enhanced build script for multi-folder notes system with automatic discovery.
Scans notes/ folder structure and generates HTML pages for all topics.
"""

import re
import os
from pathlib import Path

def parse_markdown_to_html(md_file):
    """Convert markdown file to HTML content with aman.ai-style table of contents"""
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    html_content = []
    toc_items = []
    
    # First pass: collect main topics for TOC
    for line in lines:
        line = line.rstrip()
        if not line.strip():
            continue
            
        # Main topics (no leading spaces, starts with -)
        if line.startswith('- ') and not line.startswith('-   '):
            content = line[2:].strip()
            if content and not content.startswith('-'):
                safe_content = re.sub(r'[^a-zA-Z0-9\s]', '', content).replace(' ', '-').lower()
                anchor_id = f"q-{safe_content[:30]}"
                toc_items.append({
                    'title': content,
                    'anchor': anchor_id
                })
    
    # Generate Table of Contents in aman.ai style
    if toc_items:
        html_content.append('            <div class="table-of-contents">')
        html_content.append('              <ul class="toc-list">')
        for item in toc_items:
            html_content.append(f'                <li><a href="#{item["anchor"]}">* {item["title"]}</a></li>')
        html_content.append('              </ul>')
        html_content.append('            </div>')
        html_content.append('')
    
    # Second pass: generate content with proper grouping
    current_main_topic = None
    current_subtopic = None
    in_main_list = False
    in_sub_list = False
    in_deep_list = False
    
    for line in lines:
        original_line = line
        line = line.rstrip()
        
        # Skip empty lines and titles
        if not line.strip() or line.strip().startswith('#'):
            continue
        
        # Count leading spaces
        leading_spaces = len(original_line) - len(original_line.lstrip())
        content = line.strip()
        
        # Handle references section
        if content.startswith('References & Resources:'):
            # Close any open lists
            if in_deep_list:
                html_content.append('                    </ul>')
                in_deep_list = False
            if in_sub_list:
                html_content.append('                </ul>')
                in_sub_list = False
            if in_main_list:
                html_content.append('            </ul>')
                in_main_list = False
                
            html_content.append('            <div class="references-section">')
            html_content.append('              <h3>References & Resources</h3>')
            html_content.append('              <ol class="references-list">')
            continue
        
        # Handle numbered references
        if content.startswith(('1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. ', '10. ', '11. ', '12. ', '13. ', '14. ', '15. ')):
            link_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', content)
            if link_match:
                link_text = link_match.group(1)
                link_url = link_match.group(2)
                html_content.append(f'                <li><a href="{link_url}" target="_blank" rel="noopener noreferrer">{link_text}</a></li>')
            else:
                html_content.append(f'                <li>{content}</li>')
            continue
        
        # Close references section if we hit a non-reference line
        if 'references-list' in ''.join(html_content[-5:]) and not content.startswith(('1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. ', '10. ', '11. ', '12. ', '13. ', '14. ', '15. ')):
            html_content.append('              </ol>')
            html_content.append('            </div>')
        
        # Skip if not a bullet point
        if not content.startswith('- '):
            continue
        
        # Remove the '- ' prefix
        content = content[2:].strip()
        
        # Top-level (0 spaces) - Main topics (bold headers)
        if leading_spaces == 0:
            # Close any open lists first
            if in_sub_list:
                html_content.append('                </ul>')
                in_sub_list = False
            if in_main_list:
                html_content.append('              </li>')
                html_content.append('            </ul>')
                in_main_list = False
            
            # Create anchor for main topic
            safe_content = re.sub(r'[^a-zA-Z0-9\s]', '', content).replace(' ', '-').lower()
            anchor_id = f"q-{safe_content[:30]}"
            
            # Add bold header (like in your image)
            html_content.append(f'            <p id="{anchor_id}" class="question"><strong>{content}</strong></p>')
            current_main_topic = content
            current_subtopic = None
            
        # First level indent (4 spaces) - Sub-topics
        elif leading_spaces == 4:
            # Close any deeper lists if open
            if in_deep_list:
                html_content.append('                  </ul>')
                in_deep_list = False
            if in_sub_list:
                html_content.append('                </ul>')
                in_sub_list = False
            
            # Start new sub-topic
            if not in_sub_list:
                html_content.append('            <ul style="margin-left: 1.5rem;">')
                in_sub_list = True
            
            html_content.append(f'              <li>{content}</li>')
            
        # Second level indent (8 spaces) - Sub-sub-topics
        elif leading_spaces == 8:
            # Close deeper lists if open
            if in_deep_list:
                html_content.append('                    </ul>')
                in_deep_list = False
            
            # Start sub-sub-topic list
            if not in_deep_list:
                html_content.append('                <ul style="margin-left: 1.5rem;">')
                in_deep_list = True
            
            html_content.append(f'                  <li>{content}</li>')
            
        # Third level indent (12+ spaces) - Deep nested content
        elif leading_spaces >= 12:
            if not in_deep_list:
                html_content.append('                <ul style="margin-left: 1.5rem;">')
                in_deep_list = True
            
            # Handle even deeper nesting
            nested_level = (leading_spaces - 12) // 4
            indent = '                  ' + '    ' * nested_level
            html_content.append(f'{indent}<li>{content}</li>')
    
    # Close any open lists
    if in_deep_list:
        html_content.append('                    </ul>')
    if in_sub_list:
        html_content.append('                </ul>')
    if in_main_list:
        html_content.append('            </ul>')
    
    # Close references section if it was opened
    if 'references-list' in ''.join(html_content[-10:]):
        html_content.append('              </ol>')
        html_content.append('            </div>')
    
    return '\n'.join(html_content)

def get_password():
    """No password needed - knowledge is free!"""
    return None

def discover_note_folders():
    """Discover all note folders and their markdown files"""
    # Find notes directory relative to script location
    script_dir = Path(__file__).parent
    notes_dir = script_dir / '../notes'
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
                # Remove # and any extra spaces
                return first_line[1:].strip()
            elif first_line:  # If first line exists and is not empty, use it as title
                return first_line
            else:
                return md_file.stem.replace('-', ' ').replace('_', ' ').title()
    except:
        return md_file.stem.replace('-', ' ').replace('_', ' ').title()

def create_html_template(title, content, password):
    """Create HTML template for a notes page with cache-busting"""
    import time
    cache_buster = int(time.time())
    return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>{title} - Notes</title>
    <link rel="stylesheet" href="../assets/style.css?v={cache_buster}" />
    <style>
      /* Additional styles for notes page - always visible */
      .notes-content {{
        display: block !important;
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
      
      /* Table of Contents Styles - aman.ai inspired */
      .table-of-contents {{
        margin-bottom: 2rem;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      }}
      
      .toc-list {{
        list-style: none;
        padding: 0;
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.6;
      }}
      
      .toc-list li {{
        margin-bottom: 0.3rem;
        position: relative;
      }}
      
      .toc-list a {{
        color: #007bff;
        text-decoration: none;
        display: block;
        padding: 0.1rem 0;
        transition: color 0.2s ease;
      }}
      
      .toc-list a:hover {{
        color: #0056b3;
        text-decoration: underline;
      }}
      
      .question {{
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e9ecef;
      }}
      
      /* Back to Top Button */
      .back-to-top {{
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: #007bff;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 18px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,123,255,0.3);
        transition: all 0.3s ease;
        opacity: 0;
        visibility: hidden;
        z-index: 1000;
      }}
      
      .back-to-top:hover {{
        background: #0056b3;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,123,255,0.4);
      }}
      
      .back-to-top.visible {{
        opacity: 1;
        visibility: visible;
      }}
      
      .back-to-top .icon {{
        display: inline-block;
        transform: rotate(-90deg);
      }}
      
      /* References section styling */
      .references-section {{
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 2rem;
      }}
      
      .references-section h3 {{
        margin-top: 0;
        margin-bottom: 1rem;
        color: #495057;
        font-size: 1.2rem;
      }}
      
      .references-list {{
        margin: 0;
        padding-left: 1.5rem;
      }}
      
      .references-list li {{
        margin-bottom: 0.5rem;
        line-height: 1.5;
      }}
      
      .references-list a {{
        color: #007bff;
        text-decoration: none;
        font-weight: 500;
      }}
      
      .references-list a:hover {{
        text-decoration: underline;
      }}
      
      @media (max-width: 768px) {{
        .notes-header h1 {{
          font-size: 2rem;
        }}
        .table-of-contents {{
          padding: 1rem;
        }}
        .back-to-top {{
          bottom: 20px;
          right: 20px;
          width: 45px;
          height: 45px;
          font-size: 16px;
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

    <!-- Back to Top Button -->
    <button class="back-to-top" id="backToTop" onclick="scrollToTop()" title="Back to Table of Contents">
      <span class="icon">→</span>
    </button>

    <script>
      // Notes are now freely accessible - no authentication required
      function checkAuth() {{
        // Always show content - knowledge is free!
        document.getElementById('notesContent').style.display = 'block';
      }}

      // Scroll to top functionality
      function scrollToTop() {{
        window.scrollTo({{
          top: 0,
          behavior: 'smooth'
        }});
      }}

      // Show/hide back to top button based on scroll position
      function toggleBackToTopButton() {{
        const backToTopButton = document.getElementById('backToTop');
        if (window.pageYOffset > 300) {{
          backToTopButton.classList.add('visible');
        }} else {{
          backToTopButton.classList.remove('visible');
        }}
      }}

      // Initialize page
      document.addEventListener('DOMContentLoaded', function() {{
        checkAuth();
        
        // Add scroll event listener for back to top button
        window.addEventListener('scroll', toggleBackToTopButton);
      }});
    </script>
  </body>
</html>'''

def build_notes_hub(note_structure):
    """Build the main notes hub page with simple table of contents format"""
    
    # Generate hub content
    hub_content = []
    
    for folder_name, files in note_structure.items():
        folder_title = folder_name.replace('-', ' ').replace('_', ' ').title()
        hub_content.append(f'''
          <div class="toc-section" id="{folder_name}">
            <h2>{folder_title}</h2>
            <ul class="toc-list">''')
        
        for file_info in files:
            file_title = file_info['title']
            file_name = file_info['name']
            html_file = f"../notes-html/{folder_name}-{file_name}.html"
            
            hub_content.append(f'''
              <li>
                <a href="{html_file}">{file_title}</a>
              </li>''')
        
        hub_content.append('''
            </ul>
          </div>''')
    
    # Create simple notes hub template
    hub_template = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>Notes Hub - Study Materials</title>
    <link rel="stylesheet" href="../assets/style.css" />
    <style>
      .notes-content { display: block; }
      
      .notes-header {
        text-align: center;
        margin: 2rem 0;
        padding: 2rem;
      }
      
      .notes-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: #333;
      }
      
      .notes-header .subtitle {
        color: #666;
        font-size: 1.1rem;
      }
      
      .toc-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
      }
      
      .toc-section {
        margin-bottom: 2rem;
      }
      
      .toc-section:last-child {
        margin-bottom: 0;
      }
      
      .toc-section h2 {
        font-size: 1.5rem;
        color: #333;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #ddd;
      }
      
      .toc-list {
        list-style: none;
        padding: 0;
        margin: 0;
      }
      
      .toc-list li {
        margin-bottom: 0.5rem;
      }
      
      .toc-list a {
        color: #007bff;
        text-decoration: none;
        font-weight: 500;
        font-size: 1rem;
        display: block;
        padding: 0.5rem 0;
        border-bottom: 1px solid #f0f0f0;
      }
      
      .toc-list a:hover {
        color: #0056b3;
        text-decoration: underline;
      }
      
      @media (max-width: 768px) {
        .notes-header h1 {
          font-size: 2rem;
        }
        .toc-container {
          margin: 0 1rem;
          padding: 1rem;
        }
      }
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
      <div class="notes-content" id="notesContent">
        <div class="notes-header">
          <h1>Notes Hub</h1>
          <p class="subtitle">Study materials and technical notes</p>
        </div>
        
        <div class="toc-container">
''' + ''.join(hub_content) + '''
        </div>
      </div>
    </main>
    
    <footer>
      <p>&copy; 2025 Notes Hub</p>
    </footer>

    <script>
      console.log('Notes Hub loaded');
    </script>
  </body>
</html>'''
    
    # Write the hub file
    script_dir = Path(__file__).parent
    hub_file = script_dir / '../pages/notes.html'
    
    with open(hub_file, 'w', encoding='utf-8') as f:
        f.write(hub_template)
    
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
    
    # Ensure notes-html directory exists
    script_dir = Path(__file__).parent
    output_dir = script_dir / '../notes-html'
    output_dir.mkdir(exist_ok=True)
    
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
            
            if len(md_content.strip()) < 100:
                print(f"    ⚠️  Warning: {file_title} seems too short!")
                continue
            
            # Parse markdown to HTML
            html_content = parse_markdown_to_html(md_file)
            
            # Create HTML file
            html_template = create_html_template(file_title, html_content, None)
            
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
    print(f"3. Your notes are now freely accessible to everyone!")

if __name__ == '__main__':
    main()