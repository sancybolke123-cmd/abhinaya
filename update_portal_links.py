import os
import glob

# Find all html and php files
files = glob.glob('c:/Xamp/htdocs/abhinaya/*.html') + glob.glob('c:/Xamp/htdocs/abhinaya/*.php')

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'student-portal.html' in content:
        new_content = content.replace('student-portal.html', 'student-portal.php')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(filepath)}")

print("Done updating all links to point to the new PHP portal.")
