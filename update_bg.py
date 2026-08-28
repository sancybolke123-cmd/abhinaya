import os

files = ['student-portal.html', 'registration.html', 'login.html', 'dashboard.php']
old_bg = 'background:#0a0a0a;'
new_bg = "background: linear-gradient(rgba(10, 10, 10, 0.75), rgba(10, 10, 10, 0.75)), url('https://i.pinimg.com/736x/a1/d4/55/a1d455dfb68a514b1cdcb0779246437c.jpg') center/cover no-repeat fixed;"

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        if old_bg in content:
            content = content.replace(old_bg, new_bg)
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Updated {file}')

# Also update the python generator scripts so future generations have the background
gen_files = ['generate_portal_pages.py', 'generate_dashboard.py']
old_repl_code = 'template = template.replace(\'<li><a href="#">Programs</a></li>\', \'<li><a href="#">Programs</a></li>\\n    <li><a href="student-portal.html">Students Portal</a></li>\')'
new_repl_code = old_repl_code + '\n    template = template.replace("background:#0a0a0a;", "' + new_bg + '")'

for file in gen_files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        if old_repl_code in content:
            content = content.replace(old_repl_code, new_repl_code)
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Updated {file}')
