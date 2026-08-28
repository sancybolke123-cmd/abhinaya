import re
import os

base_dir = 'c:/Xamp/htdocs/abhinaya'

with open(os.path.join(base_dir, 'home.html'), 'r', encoding='utf-8') as f:
    content = f.read()

head_match = re.search(r'(<head>.*?</head>)', content, re.DOTALL)
head_content = head_match.group(1) if head_match else ''

nav_match = re.search(r'(<nav>.*?</nav>)', content, re.DOTALL)
nav_content = nav_match.group(1) if nav_match else ''

footer_match = re.search(r'(<footer.*</footer>)', content, re.DOTALL)
footer_content = footer_match.group(1) if footer_match else ''

template = f"""<!DOCTYPE html>
<html lang="en">
{head_content}
<body>
{nav_content}

<section class="hero" style="height: 40vh; min-height: 300px;">
    <div class="hero-content">
        <h1 class="page-title" style="font-size: 3.5rem;">{{{{title}}}}</h1>
    </div>
</section>

<section class="content-section" style="min-height: 40vh; padding: 100px 10%;">
    <div class="about-box">
        <h2 style="color: #d4af37; font-family: 'Cinzel', serif; margin-bottom: 20px;">Welcome to {{{{title}}}}</h2>
        <p style="color: #ddd;">This section is under construction.</p>
    </div>
</section>

{footer_content}
</body>
</html>
"""

with open(os.path.join(base_dir, 'template.html'), 'w', encoding='utf-8') as f:
    f.write(template)

print('Template created.')

pages = [
    ("Faculty", "student-catalogue.html"),
    ("Academic Calendar", "academic-calendar.html"),
    ("Examinations", "examinations.html"),
    ("Attendance", "attendance.html"),
    ("Results", "results.html"),
    ("Certificates", "certificates.html"),
    ("Events & Workshops", "events-workshops.html"),
    ("Scholarships", "scholarships.html"),
    ("Programs", "programs.html"),
    ("Contact", "contact.html"),
    ("Fee Payment", "fee-payment.html"),
]

for title, filename in pages:
    page_content = template.replace('{{title}}', title)
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(page_content)
    print(f'Created {filename}')

