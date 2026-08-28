import os
import re

directory = "c:/Xamp/htdocs/abhinaya"

for filename in os.listdir(directory):
    if filename.endswith(".html") or filename.endswith(".php"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove the <li> tag containing the Programs link
        # This regex matches the entire line with possible leading spaces
        new_content = re.sub(r'^\s*<li><a[^>]*>Programs</a></li>\s*\n?', '', content, flags=re.MULTILINE)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Removed Programs link from {filename}")
