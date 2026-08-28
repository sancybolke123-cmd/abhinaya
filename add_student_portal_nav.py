import os
import glob

files = glob.glob("*.html") + glob.glob("*.php")

student_portal_item = '    <li><a href="student-portal.html">Students Portal</a></li>\n'

for filepath in files:
    if os.path.isfile(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Check if it already has the link
            has_portal_link = any('Students Portal' in line for line in lines)
            
            if not has_portal_link:
                new_lines = []
                inserted = False
                for line in lines:
                    new_lines.append(line)
                    # if the line contains Programs, add Students Portal right after it
                    if '>Programs</a>' in line and not inserted:
                        new_lines.append(student_portal_item)
                        inserted = True
                
                if inserted:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    print(f"Added to {filepath}")
        except Exception as e:
            print(f"Skipped {filepath}: {e}")
