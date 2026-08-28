import os
import glob
import re

def update_academic_calendar_links():
    directory = 'c:/Xamp/htdocs/abhinaya'
    extensions = ['*.html', '*.php']
    
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(directory, ext)))
        
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Regex to match the Academic Calendar link
            # It could be href="#" or href="academic-calendar.html" or href="academic-calendra.html"
            # We want to replace it with href="ACADEMIC CALENDAR.pdf" target="_blank"
            
            # Match `<a href="...">Academic Calendar</a>`
            # Using regex: `<a\s+href="[^"]*"\s*>Academic Calendar</a>`
            # Some might already have target="_blank" so let's match `<a\s+href="[^"]*"(?:\s+target="[^"]*")?\s*>Academic Calendar</a>`
            # and replace with `<a href="ACADEMIC CALENDAR.pdf" target="_blank">Academic Calendar</a>`
            
            pattern = re.compile(r'<a\s+href="[^"]*"(?:\s+target="[^"]*")?\s*>Academic Calendar</a>', re.IGNORECASE)
            
            new_content = pattern.sub('<a href="ACADEMIC CALENDAR.pdf" target="_blank">Academic Calendar</a>', content)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {os.path.basename(file_path)}")
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    update_academic_calendar_links()
