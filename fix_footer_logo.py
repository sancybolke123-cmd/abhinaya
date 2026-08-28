import glob
import re

files = glob.glob('c:/Xamp/htdocs/abhinaya/*.html') + glob.glob('c:/Xamp/htdocs/abhinaya/*.php')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    if '.footer-logo{\n    width:120px;' in content:
        content = content.replace('.footer-logo{\n    width:120px;', '.footer-logo{\n    width:70px;')
        modified = True
    elif 'width: 120px;' in content and '.footer-logo' in content:
        # regex replacement for safety
        new_content = re.sub(r'(\.footer-logo\s*{[^}]*width:\s*)120px', r'\1 70px', content)
        if new_content != content:
            content = new_content
            modified = True
        
    if modified:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated footer logo in", file)
