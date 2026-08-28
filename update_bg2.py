import os

file_path = r'c:\Xamp\htdocs\abhinaya\home.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add the opening wrapper div before core-values
old_core_values = '<section class="content-section core-values"'
new_core_values = """<div style="background: linear-gradient(rgba(10,10,10,0.85), rgba(10,10,10,0.85)), url('https://i.pinimg.com/736x/26/dc/d5/26dcd58af1e08f967bcc416b47e493e9.jpg') center/cover no-repeat fixed;">
<section class="content-section core-values\""""

content = content.replace(old_core_values, new_core_values)

# 2. Add the closing div before the footer
old_footer = '<footer class="footer">'
new_footer = '</div>\n\n<footer class="footer">'

content = content.replace(old_footer, new_footer)

# 3. Remove conflicting backgrounds from child sections so the new background shows through
content = content.replace("background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1516280440614-37939bbacd81?auto=format&fit=crop&w=1200&q=80') center/cover fixed;", "background: transparent;")

content = content.replace('background: #0a0a0a;', 'background: transparent;')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Background wrapper added successfully!")
