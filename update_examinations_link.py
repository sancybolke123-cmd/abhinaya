import os
import re

directory = "c:/Xamp/htdocs/abhinaya"

for filename in os.listdir(directory):
    if filename.endswith(".html") or filename.endswith(".php"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace href="#" or anything else for Examinations to href="examinations.html"
        new_content = re.sub(r'<a\s+href="[^"]*"\s*>Examinations</a>', r'<a href="examinations.html">Examinations</a>', content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")
