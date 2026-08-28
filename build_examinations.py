import re

with open('c:/Xamp/htdocs/abhinaya/home.html', 'r', encoding='utf-8') as f:
    home = f.read()

nav_match = re.search(r'<nav>.*?</nav>', home, re.DOTALL)
footer_match = re.search(r'<footer[^>]*>.*?</footer>', home, re.DOTALL)

nav_html = nav_match.group(0) if nav_match else ''
footer_html = footer_match.group(0) if footer_match else ''

pdfs = [
    ("AIRF Diploma 1", "ABHINAYAA-DIP-1-Question-Paper.pdf"),
    ("AIRF Diploma 2", "ABHINAYAA-DIP-2-Question-paper.pdf"),
    ("AIRF NP 1", "ABHINAYAA-NP-1-QUESTION-PAPER.pdf"),
    ("AIRF NP 2", "ABHINAYAA-NP-2-Question-paper.pdf"),
    ("Diploma 1 – 2020", "Diploma-1-question-paper-2020.pdf"),
    ("Diploma 2 – 2020", "Diploma-2-question-paper-2020.pdf"),
    ("Master Diploma 1", "MASTER-DIPLOMA-1-Question-Paper.pdf"),
    ("Master Diploma 1 – 2018", "MD-I-Question-Paper-2018.pdf"),
    ("Master Diploma 2 – 2018", "MD-II-Question-Paper-2018.pdf"),
    ("Nritya Prabha", "NRITYA-PRABHA.pdf"),
    ("Diploma 2 – 2024", "DIPLOMA-Question-paper-2024.pdf"),
    ("Diploma 1 & 2", "Questions-for-DIPOMA-2022.pdf"),
    ("Diploma 1 – 2017", "Questions-for-DIPOMA-03122017.pdf"),
    ("Diploma 1 & 2", "Questions-for-DIPOMA.pdf"),
    ("Visharad 1", "Visharad-I.pdf")
]

grid_items = ''
for title, file in pdfs:
    grid_items += f'''
        <a href="{file}" target="_blank" class="pdf-card reveal">
            <i class="fa fa-file-pdf-o"></i>
            <p>{title}</p>
        </a>
    '''

exam_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Examinations - Abhinaya Institute</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; }}
        body {{
            font-family: 'Poppins', sans-serif;
            background:#0a0a0a;
            color: white;
            overflow-x: hidden;
        }}
        body::before {{
            content: ''; position: fixed; width: 400px; height: 400px; background: #d4af37;
            border-radius: 50%; filter: blur(180px); top: -150px; left: -100px; opacity: 0.20; z-index: -1;
        }}
        body::after {{
            content: ''; position: fixed; width: 350px; height: 350px; background: #8b0000;
            border-radius: 50%; filter: blur(180px); right: -100px; bottom: -100px; opacity: 0.15; z-index: -1;
        }}
        
        /* Navbar */
        nav {{
            position: fixed; top: 0; width: 100%; display: flex; justify-content: space-between;
            align-items: center; padding: 20px 70px; background: rgba(0, 0, 0, 0.25);
            backdrop-filter: blur(15px); z-index: 999;
        }}
        .logo {{ display: flex; align-items: center; font-family: 'Cinzel', serif; font-size: 1.5rem; font-weight: 700; color: #d4af37; text-decoration: none; }}
        nav ul {{ display: flex; gap: 30px; list-style: none; align-items: center; }}
        nav ul li a {{ color: white; text-decoration: none; transition: 0.3s; font-weight: 500; }}
        nav ul li a:hover {{ color: #d4af37; }}
        
        /* Dropdown Styles */
        .dropdown {{ position: relative; }}
        .dropdown-content {{
            display: none; position: absolute; background: rgba(10, 10, 10, 0.95); min-width: 200px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.5); border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 10px; overflow: hidden; top: 100%; left: 0; z-index: 1000;
        }}
        .dropdown-content a {{
            color: white; padding: 12px 16px; text-decoration: none; display: block;
            border-bottom: 1px solid rgba(255,255,255,0.05); transition: 0.3s;
        }}
        .dropdown-content a:hover {{ background-color: rgba(212, 175, 55, 0.1); color: #d4af37; }}
        .dropdown:hover .dropdown-content {{ display: block; }}
        
        /* Hero Section */
        .hero {{
            height: 60vh; min-height: 500px; display: flex; align-items: center; justify-content: flex-start;
            text-align: left; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.8)), url('https://abhinayaainstitute.org/wp-content/uploads/2026/06/Exam-Banner.jpg') center/cover;
            padding: 0 10%; padding-top: 80px;
        }}
        .hero-content h1 {{ font-family: 'Cinzel', serif; font-size: 5rem; color: #d4af37; margin-bottom: 20px; text-shadow: 2px 2px 10px rgba(0,0,0,0.8); }}
        .hero-content p {{ font-size: 1.4rem; color: #ddd; margin-bottom: 30px; max-width: 600px; }}
        
        /* Content Sections */
        .content-section {{ padding: 80px 10%; }}
        .section-title {{ font-family: 'Cinzel', serif; color: #d4af37; font-size: 3rem; margin-bottom: 30px; }}
        
        .btn-primary {{
            display: inline-block; background: linear-gradient(135deg, #d4af37, #f8d76d); color: #0a0a0a;
            padding: 15px 35px; text-decoration: none; font-weight: 600; font-size: 1.1rem;
            border-radius: 50px; transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 5px 15px rgba(212,175,55,0.3);
        }}
        .btn-primary:hover {{ transform: scale(1.05); box-shadow: 0 8px 20px rgba(212,175,55,0.5); }}
        
        .marksheet-box {{
            background: rgba(255,255,255,0.03); border: 1px solid rgba(212,175,55,0.2);
            padding: 50px; border-radius: 20px; text-align: center; margin-bottom: 80px;
            border-top: 4px solid #d4af37;
        }}
        
        .pdf-grid {{
            display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 30px;
        }}
        .pdf-card {{
            background: rgba(255,255,255,0.05); padding: 30px 20px; border-radius: 15px;
            text-align: center; color: white; text-decoration: none; transition: 0.4s;
            border: 1px solid transparent; display: flex; flex-direction: column; align-items: center; gap: 15px;
        }}
        .pdf-card:hover {{
            background: rgba(212,175,55,0.1); border-color: rgba(212,175,55,0.4); transform: translateY(-5px);
        }}
        .pdf-card i {{ font-size: 3rem; color: #d4af37; }}
        .pdf-card p {{ font-weight: 500; font-size: 1.1rem; }}
        
        .contact-box {{
            background: #6A0A00; padding: 60px 10%; margin-top: 80px;
            display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 30px;
        }}
        
        /* Scroll Reveal Animations */
        .reveal {{ opacity: 0; transform: translateY(40px); transition: opacity 0.8s ease-out, transform 0.8s ease-out; }}
        .reveal.active {{ opacity: 1; transform: translateY(0); }}
        .reveal-left {{ opacity: 0; transform: translateX(-50px); transition: opacity 0.8s ease-out, transform 0.8s ease-out; }}
        .reveal-left.active {{ opacity: 1; transform: translateX(0); }}
        .reveal-right {{ opacity: 0; transform: translateX(50px); transition: opacity 0.8s ease-out, transform 0.8s ease-out; }}
        .reveal-right.active {{ opacity: 1; transform: translateX(0); }}
    </style>
</head>
<body>

{nav_html}

<section class="hero">
    <div class="hero-content reveal-left">
        <h1>Examinations</h1>
        <p>Access examination papers and marksheet guidelines.</p>
    </div>
</section>

<section class="content-section">
    <div class="marksheet-box reveal">
        <h2 class="section-title" style="margin-bottom: 15px;">Marksheet Structure</h2>
        <p style="font-size: 1.2rem; color: #ddd; margin-bottom: 30px; font-style: italic;">View the marks distribution and evaluation criteria for each examination level.</p>
        <a href="MARKSHEET-STRUCTURE.pdf" target="_blank" class="btn-primary">
            <i class="fa fa-download" style="margin-right: 10px;"></i> Download Structure
        </a>
    </div>

    <h2 class="section-title reveal" style="text-align: center; margin-bottom: 50px;">Examination Question Papers</h2>
    <div class="pdf-grid">
        {grid_items}
    </div>
</section>

<section class="contact-box">
    <div class="reveal-left">
        <h6 style="color: #f8d76d; font-size: 1.2rem; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px;">Academic Services</h6>
        <h2 style="font-family: 'Cinzel', serif; font-size: 2.5rem; color: white; margin-bottom: 15px;">Examination & Certification Support</h2>
        <p style="color: #ddd; font-size: 1.1rem; max-width: 500px;">For examination-related assistance, certificates, and academic queries, kindly mail to:</p>
    </div>
    <div class="reveal-right">
        <a href="mailto:exams@abhinayaainstitute.org" class="btn-primary" style="background: transparent; border: 2px solid #d4af37; color: #d4af37; padding: 15px 40px; box-shadow: none;">
            exams@abhinayaainstitute.org <i class="fa fa-arrow-right" style="margin-left: 10px;"></i>
        </a>
    </div>
</section>

{footer_html}

<script>
document.addEventListener("DOMContentLoaded", function() {{
    var reveals = document.querySelectorAll(".reveal, .reveal-left, .reveal-right");
    var observer = new IntersectionObserver(function(entries, observer) {{
        entries.forEach(function(entry) {{
            if (entry.isIntersecting) {{
                entry.target.classList.add("active");
                observer.unobserve(entry.target);
            }}
        }});
    }}, {{ rootMargin: "0px 0px -30px 0px" }});
    
    reveals.forEach(function(reveal) {{
        observer.observe(reveal);
    }});
}});
</script>

</body>
</html>
"""

with open('c:/Xamp/htdocs/abhinaya/examinations.html', 'w', encoding='utf-8') as f:
    f.write(exam_html)

print("Successfully generated examinations.html")
