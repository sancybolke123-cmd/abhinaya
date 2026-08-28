import os
import glob

# Keywords to look for
targets = [
]

# Get all HTML and PHP files
files = glob.glob("*.html") + glob.glob("*.php")
# Also check template files or python generator files if they contain these tags directly
files.extend(glob.glob("*.py"))

for filepath in files:
    if os.path.isfile(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            new_lines = []
            modified = False
            
            for line in lines:
                # If any target string is in the line, we skip adding it to new_lines
                # but only if it's in the navigation context (e.g. not breaking something else)
                # However, since these are very specific link texts, it should be safe.
                should_remove = False
                for target in targets:
                    if target.lower() in line.lower():
                        should_remove = True
                        modified = True
                        break
                
                if not should_remove:
                    new_lines.append(line)
                    
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f"Updated {filepath}")
        except Exception as e:
            print(f"Skipped {filepath}: {e}")
