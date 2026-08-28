import os
import glob

# Find all html and php files
files = glob.glob('c:/Xamp/htdocs/abhinaya/*.html') + glob.glob('c:/Xamp/htdocs/abhinaya/*.php')

target = 'var reveals = document.querySelectorAll(".reveal, .reveal-left, .reveal-right");'
replacement = 'var reveals = document.querySelectorAll(".reveal, .reveal-left, .reveal-right, footer");'

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if target in content:
        new_content = content.replace(target, replacement)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed footer reveal observer in {os.path.basename(filepath)}")

print("Done updating all reveal observers!")
