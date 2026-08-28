import glob

files = glob.glob('c:/Xamp/htdocs/abhinaya/*.html') + glob.glob('c:/Xamp/htdocs/abhinaya/*.php')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    if 'href="#gallery"' in content:
        content = content.replace('href="#gallery"', 'href="gallery.html"')
        modified = True
    if 'href="#">Gallery' in content:
        content = content.replace('href="#">Gallery', 'href="gallery.html">Gallery')
        modified = True
        
    if modified:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated links in", file)
