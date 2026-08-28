import re

with open('c:/Xamp/htdocs/abhinaya/template.html', 'r', encoding='utf-8') as f:
    t = f.read()

nav_match = re.search(r'<nav>.*?</nav>', t, re.DOTALL)
footer_match = re.search(r'<footer class="footer">.*?</footer>', t, re.DOTALL)

with open('c:/Xamp/htdocs/abhinaya/guru.html', 'r', encoding='utf-8') as f:
    g = f.read()

# Replace nav
if nav_match:
    g = re.sub(r'<nav>.*?</nav>', nav_match.group(0), g, flags=re.DOTALL)

# Replace footer
if footer_match:
    g = re.sub(r'<footer>.*?</footer>', footer_match.group(0), g, flags=re.DOTALL)

# Fix accordion JS
g = g.replace('querySelectorAll(".accordion")', 'querySelectorAll(".award-btn")')
g = g.replace('querySelectorAll(".panel")', 'querySelectorAll(".award-content")')

with open('c:/Xamp/htdocs/abhinaya/guru.html', 'w', encoding='utf-8') as f:
    f.write(g)
print('Updated guru.html')
