import re
import glob

# Read the correct nav from home.html
with open('c:/Xamp/htdocs/abhinaya/home.html', 'r', encoding='utf-8') as f:
    home_content = f.read()

nav_match = re.search(r'<nav>.*?</nav>', home_content, re.DOTALL | re.IGNORECASE)

if nav_match:
    correct_nav = nav_match.group(0)
    
    # Get all html and php files
    files = glob.glob('c:/Xamp/htdocs/abhinaya/*.html') + glob.glob('c:/Xamp/htdocs/abhinaya/*.php')
    
    for filepath in files:
        # skip home.html since it's already correct
        if 'home.html' in filepath:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the nav
        if re.search(r'<nav>.*?</nav>', content, re.DOTALL | re.IGNORECASE):
            new_content = re.sub(r'<nav>.*?</nav>', correct_nav, content, flags=re.DOTALL | re.IGNORECASE)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated nav in {filepath}")
    print("Successfully updated navigation across all pages.")
else:
    print("Could not find nav in home.html!")
