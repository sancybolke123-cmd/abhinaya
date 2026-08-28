import os
import re

directory = "c:/Xamp/htdocs/abhinaya"

for filename in os.listdir(directory):
    if filename.endswith(".html") or filename.endswith(".php"):
        if filename == "contact.php":
            continue
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace href="contact.php" with href="contact.html" for Contact links
        new_content = content.replace('href="contact.php"', 'href="contact.html"')
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Updated {filename}")
