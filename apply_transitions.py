import os
import glob
import re

# Find all html and php files
files = glob.glob('c:/Xamp/htdocs/abhinaya/*.html') + glob.glob('c:/Xamp/htdocs/abhinaya/*.php')

css_override = """
<style>
/* Global Premium Transitions Override */
nav {
    transform: translateY(-100%);
    animation: slideDown 0.8s cubic-bezier(0.165, 0.84, 0.44, 1) forwards !important;
}
@keyframes slideDown {
    from { transform: translateY(-100%); }
    to { transform: translateY(0); }
}
nav ul li a {
    position: relative;
    padding-bottom: 5px;
    transition: color 0.3s !important;
}
nav ul li a::after {
    content: '';
    position: absolute;
    width: 100%;
    transform: scaleX(0);
    height: 2px;
    bottom: 0;
    left: 0;
    background-color: #d4af37;
    transform-origin: bottom right;
    transition: transform 0.3s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
}
nav ul li a:hover::after {
    transform: scaleX(1);
    transform-origin: bottom left;
}
.dropdown-content {
    display: block !important;
    opacity: 0;
    visibility: hidden;
    transform: translateY(15px);
    transition: opacity 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), visibility 0.4s !important;
    top: 105% !important;
}
.dropdown:hover .dropdown-content {
    opacity: 1 !important;
    visibility: visible !important;
    transform: translateY(0) !important;
}
footer.footer {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 1s cubic-bezier(0.165, 0.84, 0.44, 1), transform 1s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
}
footer.footer.active {
    opacity: 1 !important;
    transform: translateY(0) !important;
}
</style>
"""

js_pattern = r"querySelectorAll\(\s*(['\"])(h2, h3, p:not\(\.hero-content p\):not\(footer p\):not\(\.footer-bottom p\), \.gallery-card, \.student-card, \.about-box, \.course-card, img:not\(nav img\):not\(footer img\))\1\s*\)"

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    modified = False
    
    # Inject CSS overrides if not already present
    if 'Global Premium Transitions Override' not in content:
        if '</head>' in content:
            content = content.replace('</head>', f'{css_override}</head>')
            modified = True
            
    # Update JS query selector to include footer
    if re.search(js_pattern, content):
        content = re.sub(js_pattern, r"querySelectorAll(\1\2, footer\1)", content)
        modified = True
        
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Applied beautiful transitions to {os.path.basename(filepath)}")

print("Transitions setup complete globally!")
