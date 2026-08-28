import os

directory = "c:/Xamp/htdocs/abhinaya"

for filename in os.listdir(directory):
    if filename.endswith(".html") or filename.endswith(".php"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # We only want to replace contact.html with contact.php in links
        if 'href="contact.html"' in content:
            new_content = content.replace('href="contact.html"', 'href="contact.php"')
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Updated {filename}")
