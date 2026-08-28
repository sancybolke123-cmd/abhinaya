import os
import glob

directory = r'c:\Xamp\htdocs\abhinaya'

files = glob.glob(os.path.join(directory, '*.html')) + glob.glob(os.path.join(directory, '*.php'))

replacements = {
    '<a href="#">Events & Workshops</a>': '<a href="events-workshops.html">Events & Workshops</a>',
    '<a href="event-workshops.html">Events & Workshops</a>': '<a href="events-workshops.html">Events & Workshops</a>',
    '<a href="#">Events</a>': '<a href="events-workshops.html">Events</a>',
    '<a href="events.html">Events</a>': '<a href="events-workshops.html">Events</a>',
}

for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        for old, new in replacements.items():
            new_content = new_content.replace(old, new)
            
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {os.path.basename(file_path)}")
    except Exception as e:
        print(f"Error processing {os.path.basename(file_path)}: {e}")

print("All event links updated successfully!")
