import glob
import re

files = glob.glob('c:/Xamp/htdocs/abhinaya/*.html') + glob.glob('c:/Xamp/htdocs/abhinaya/*.php')

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The string to remove is exactly what was injected:
    # <a href="core-team.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">Core Team</a>
    # Or something similar. I will use a regex to be safe.
    
    # Let's remove the entire line containing "Core Team</a>" in the footer links
    pattern = re.compile(r'\s*<a href="core-team\.html"[^>]*>Core Team</a>', re.IGNORECASE)
    
    if pattern.search(content):
        new_content = pattern.sub('', content)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Removed Core Team from {filepath}")
    
print("Successfully removed Core Team link from footer in all files.")
