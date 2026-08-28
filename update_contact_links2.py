import os
import re

directory = "c:/Xamp/htdocs/abhinaya"

for filename in os.listdir(directory):
    if filename.endswith(".html") or filename.endswith(".php"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace href="#" with href="contact.php" for Contact links
        new_content = re.sub(r'href="[^"]*"\s*>Contact</a>', r'href="contact.php">Contact</a>', content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Updated {filename}")
