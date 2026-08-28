import re
import glob

# Get all html and php files
files = glob.glob('c:/Xamp/htdocs/abhinaya/*.html') + glob.glob('c:/Xamp/htdocs/abhinaya/*.php')

count = 0
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to remove "Abhinaya Institute" and the margin-right on the image.
    # Because whitespace can vary, we use regex.
    # Match: <a href="home.html" class="logo"> ... </a>
    # Inside it, find the img and text
    
    pattern = r'(<a href="home\.html" class="logo">\s*<img[^>]*?)( margin-right:\s*10px;)?("[^>]*>)\s*Abhinaya Institute\s*(</a>)'
    
    # The image has style="max-width:70px !important; margin-right: 10px;"
    # Let's just do a simpler string replacement for the exact block from home.html
    
    exact_old = """<a href="home.html" class="logo">
        <img src="https://abhinayaainstitute.org/wp-content/uploads/2025/10/AIRF-Favicon.png" alt="Abhinaya Logo" style="max-width:70px !important; margin-right: 10px;">
        Abhinaya Institute
    </a>"""
    
    exact_new = """<a href="home.html" class="logo">
        <img src="https://abhinayaainstitute.org/wp-content/uploads/2025/10/AIRF-Favicon.png" alt="Abhinaya Logo" style="max-width:70px !important;">
    </a>"""
    
    if exact_old in content:
        new_content = content.replace(exact_old, exact_new)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Updated {filepath}")
    else:
        # Try regex if exact match fails due to slight whitespace differences
        regex_pattern = re.compile(r'(<a href="home\.html" class="logo">\s*<img[^>]*?)(\s*margin-right:\s*10px;?)([^>]*>\s*)Abhinaya Institute(\s*</a>)', re.IGNORECASE)
        if regex_pattern.search(content):
            new_content = regex_pattern.sub(r'\1\3\4', content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f"Updated {filepath} via regex")

print(f"Successfully removed text from {count} files.")
