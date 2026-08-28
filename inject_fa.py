import os
import glob

files = glob.glob('c:/Xamp/htdocs/abhinaya/*.html') + glob.glob('c:/Xamp/htdocs/abhinaya/*.php')
link_tag = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">\n'

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'font-awesome' not in content and '</head>' in content:
        content = content.replace('</head>', link_tag + '</head>')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Updated', os.path.basename(file))
