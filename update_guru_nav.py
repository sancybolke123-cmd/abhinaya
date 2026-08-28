import re

with open('c:/Xamp/htdocs/abhinaya/home.html', 'r', encoding='utf-8') as f:
    home_content = f.read()

# Extract the correct nav from home.html
nav_match = re.search(r'<nav>.*?</nav>', home_content, re.DOTALL)
if nav_match:
    correct_nav = nav_match.group(0)
    
    with open('c:/Xamp/htdocs/abhinaya/guru.html', 'r', encoding='utf-8') as f:
        guru_content = f.read()
    
    # Replace the old nav in guru.html
    new_guru_content = re.sub(r'<nav>.*?</nav>', correct_nav, guru_content, flags=re.DOTALL)
    
    with open('c:/Xamp/htdocs/abhinaya/guru.html', 'w', encoding='utf-8') as f:
        f.write(new_guru_content)
    print("Successfully updated guru.html's navigation bar.")
else:
    print("Failed to find nav in home.html")
