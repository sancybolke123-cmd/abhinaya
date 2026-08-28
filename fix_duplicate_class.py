import glob
import re

files = glob.glob('c:/Xamp/htdocs/abhinaya/*.html') + glob.glob('c:/Xamp/htdocs/abhinaya/*.php')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We look for <img class="reveal" ... class="footer-logo"> and fix it.
    # The safest way is to replace the exact HTML pattern generated in the footer.
    
    old_pattern_1 = '<img class="reveal" src="https://abhinayaainstitute.org/wp-content/uploads/2025/10/AIRF-Favicon.png"\n                 alt="AIRF Logo"\n                 class="footer-logo">'
    new_pattern_1 = '<img src="https://abhinayaainstitute.org/wp-content/uploads/2025/10/AIRF-Favicon.png"\n                 alt="AIRF Logo"\n                 class="footer-logo reveal">'

    old_pattern_2 = '<img class="reveal" src="https://abhinayaainstitute.org/wp-content/uploads/2025/10/AIRF-Favicon.png"\n                 alt="AIRF Logo"\n                 class="footer-logo">'
    # Let's just use regex for safety:
    
    new_content = re.sub(r'<img class="reveal" src="([^"]+)"\s*alt="AIRF Logo"\s*class="footer-logo">', r'<img src="\1" alt="AIRF Logo" class="footer-logo reveal">', content, flags=re.IGNORECASE)
    
    # Also if it's on multiple lines
    new_content = re.sub(r'<img class="reveal" src="([^"]+)"[^>]*class="footer-logo">', r'<img src="\1" alt="AIRF Logo" class="footer-logo reveal">', new_content, flags=re.IGNORECASE|re.DOTALL)
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('Fixed double class in', file)
