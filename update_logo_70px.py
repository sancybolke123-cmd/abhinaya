import glob
import re

files = glob.glob('c:/Xamp/htdocs/abhinaya/*.html') + glob.glob('c:/Xamp/htdocs/abhinaya/*.php')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Change max-width:50px to max-width:70px
    new_content = content.replace('max-width:50px !important;', 'max-width:70px !important;')
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('Updated size to 70px in', file)
