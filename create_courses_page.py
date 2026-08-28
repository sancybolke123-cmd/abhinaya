import re

with open('c:/Xamp/htdocs/abhinaya/home.html', 'r', encoding='utf-8') as f:
    home = f.read()

nav_match = re.search(r'<nav>.*?</nav>', home, re.DOTALL)
footer_match = re.search(r'<footer[^>]*>.*?</footer>', home, re.DOTALL)

nav_html = nav_match.group(0) if nav_match else ''
nav_html = nav_html.replace('student-portal.html', 'student-portal.php')
footer_html = footer_match.group(0) if footer_match else ''

courses_data = [
    ("Fresh Admission (Beginner)", "Foundation Level", "Introduction to basic body postures (Araimandi, Samapada), fundamental hand gestures (Asamyutta Hastas), eye movements, and foundational Adavus (Tatta Adavu)."),
    ("Prarambhik", "Elementary Level", "Mastery of primary Adavus including Natta Adavu, Kuditta Mettu, and Paraval Adavu. Introduction to basic Tala rhythm concepts and introductory slokas from Abhinaya Darpana."),
    ("Praveshika Pratham", "Intermediate I", "Advanced Adavu patterns, speed variations (Kala), introductory Korvais, Samyutta Hastas (combined hand gestures), and head/neck movements (Shiro & Greeva Bheda)."),
    ("Praveshika Purna", "Intermediate II", "Introduction to simple repertoire items like Alarippu (Tisra, Chatusra, or Misra) and Kautuvam. Basic understanding of Natyashastra theory and rhythm cycles."),
    ("Madhyama Pratham", "Junior Diplomatic I", "Performance of Jatiswaram and Shabdam. Nuances of expressive dance (Abhinaya), character portrayal, and study of musical ragas and talas."),
    ("Madhyama Purna", "Junior Diplomatic II", "Detailed training in central repertoire pieces such as Varnam. Balancing intricate Nritta (pure dance footwork) with deeper emotive Sanchari Bhavas."),
    ("Visharad Pratham", "Senior Graduate I", "In-depth Varnam choreography, Padams, and Ashtapadis. Advanced study of Navarasas (nine classical emotions), Natya theory, and musical accompaniment."),
    ("Visharad Dwitiya", "Senior Graduate II", "Advanced repertoire including complex Padams, Keerthanams, and energetic Tillanas. Theory on stage presentation, Aharya (costumes/makeup), and Tala calculations."),
    ("Visharad Tritiya", "Pre-Graduation Level", "Mastery of full Margam performance. Detailed analytical study of classical treatises, choreographic structuring, and Nattuvangam rhythm recital."),
    ("Alankar Pratham", "Mastery & Artistry", "Post-graduate professional training focusing on thematic productions, solo stage presence, lecture demonstrations, and pedagogical mastery for future gurus.")
]

cards_html = ""
for idx, (title, level, desc) in enumerate(courses_data, 1):
    cards_html += f"""
        <div class="course-card reveal" style="background: rgba(255,255,255,0.05); backdrop-filter: blur(15px); border: 1px solid rgba(212,175,55,0.25); border-radius: 18px; padding: 30px; text-align: left; transition: transform 0.3s, border-color 0.3s, box-shadow 0.3s; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; width: 5px; height: 100%; background: linear-gradient(180deg, #d4af37, #8b0000);"></div>
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <span style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: #d4af37; background: rgba(212,175,55,0.1); padding: 4px 12px; border-radius: 20px; font-weight: 600;">{level}</span>
                <span style="font-family: 'Cinzel', serif; font-size: 1.2rem; color: rgba(212,175,55,0.5); font-weight: 700;">#{idx:02d}</span>
            </div>
            <h3 style="font-family: 'Cinzel', serif; font-size: 1.5rem; color: white; margin-bottom: 12px;">{title}</h3>
            <p style="color: #ccc; font-size: 0.98rem; line-height: 1.7; margin-bottom: 0;">{desc}</p>
        </div>
    """

courses_php = f"""<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Course Catalogue - Abhinaya Institute</title>
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
        /* Background Glow */
        body::before {{
            content: '';
            position: fixed;
            width: 400px;
            height: 400px;
            background: #d4af37;
            border-radius: 50%;
            filter: blur(180px);
            top: -150px;
            left: -100px;
            opacity: 0.20;
            z-index: -1;
        }}
        body::after {{
            content: '';
            position: fixed;
            width: 350px;
            height: 350px;
            background: #8b0000;
            border-radius: 50%;
            filter: blur(180px);
            right: -100px;
            bottom: -100px;
            opacity: 0.15;
            z-index: -1;
        }}
        /* Navbar */
        nav {{
            position: fixed;
            top: 0;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 70px;
            background: rgba(0, 0, 0, 0.25);
            backdrop-filter: blur(15px);
            z-index: 999;
        }}
        .logo {{ display: flex; align-items: center; font-family: 'Cinzel', serif; font-size: 1.5rem; font-weight: 700; color: #d4af37; text-decoration: none; }}
        nav ul {{ display: flex; gap: 30px; list-style: none; align-items: center; }}
        nav ul li a {{ color: white; text-decoration: none; transition: 0.3s; font-weight: 500; }}
        nav ul li a:hover {{ color: #d4af37; }}
        
        .dropdown {{ position: relative; }}
        .dropdown-content {{
            display: none;
            position: absolute;
            background: rgba(10, 10, 10, 0.95);
            min-width: 200px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.5);
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 10px;
            overflow: hidden;
            top: 100%;
            left: 0;
            z-index: 1000;
        }}
        .dropdown-content a {{
            color: white;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            transition: 0.3s;
        }}
        .dropdown-content a:hover {{
            background-color: rgba(212, 175, 55, 0.1);
            color: #d4af37;
        }}
        .dropdown:hover .dropdown-content {{ display: block; }}
        
        /* Hero Section */
        .hero {{
            height: 45vh;
            min-height: 320px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.8)), url('images/slide3.jpg.jpg') center/cover;
            padding-top: 80px;
        }}
        .hero-content h1 {{
            font-family: 'Cinzel', serif;
            font-size: 3.5rem;
            color: #d4af37;
            margin-bottom: 10px;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
        }}
        .course-card:hover {{
            transform: translateY(-7px);
            border-color: #d4af37;
            box-shadow: 0 12px 25px rgba(212, 175, 55, 0.15);
        }}
        
        .footer {{
            background: #5b180f;
            padding: 50px 8% 20px;
        }}
    </style>

<style>
/* Global Premium Transitions Override */
nav {{
    transform: translateY(-100%);
    animation: slideDown 0.8s cubic-bezier(0.165, 0.84, 0.44, 1) forwards !important;
}}
@keyframes slideDown {{
    from {{ transform: translateY(-100%); }}
    to {{ transform: translateY(0); }}
}}
nav ul li a {{
    position: relative;
    padding-bottom: 5px;
    transition: color 0.3s !important;
}}
nav ul li a::after {{
    content: '';
    position: absolute;
    width: 100%;
    transform: scaleX(0);
    height: 2px;
    bottom: 0;
    left: 0;
    background-color: #d4af37;
    transform-origin: bottom right;
    transition: transform 0.3s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
}}
nav ul li a:hover::after {{
    transform: scaleX(1);
    transform-origin: bottom left;
}}
.dropdown-content {{
    display: block !important;
    opacity: 0;
    visibility: hidden;
    transform: translateY(15px);
    transition: opacity 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), visibility 0.4s !important;
    top: 105% !important;
}}
.dropdown:hover .dropdown-content {{
    opacity: 1 !important;
    visibility: visible !important;
    transform: translateY(0) !important;
}}
footer.footer {{
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 1s cubic-bezier(0.165, 0.84, 0.44, 1), transform 1s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
}}
footer.footer.active {{
    opacity: 1 !important;
    transform: translateY(0) !important;
}}
</style>
</head>
<body>
{nav_html}

<section class="hero">
    <div class="hero-content">
        <h1 class="page-title">Curriculum & Courses</h1>
        <p style="color: #ddd; font-size: 1.1rem; max-width: 600px; margin: auto;">Explore our comprehensive classical Bharatanatyam syllabus, spanning from foundational steps to professional mastery.</p>
        <?php if(isset($_SESSION['user_id'])): ?>
            <div style="margin-top: 20px;">
                <a href="dashboard.php" style="display: inline-block; background: transparent; border: 2px solid #d4af37; color: #d4af37; padding: 8px 24px; border-radius: 50px; text-decoration: none; font-weight: 500; transition: 0.3s;"><i class="fa fa-arrow-left"></i> Back to Dashboard</a>
            </div>
        <?php endif; ?>
    </div>
</section>

<section style="padding: 70px 8%; max-width: 1300px; margin: auto;">
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 30px;">
        {cards_html}
    </div>
</section>

{footer_html}

<script>
document.addEventListener("DOMContentLoaded", function() {{
    var reveals = document.querySelectorAll(".reveal, .reveal-left, .reveal-right, footer");
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

with open('c:/Xamp/htdocs/abhinaya/courses.php', 'w', encoding='utf-8') as f:
    f.write(courses_php)

print("Created courses.php successfully!")

# Update dashboard.php link
with open('c:/Xamp/htdocs/abhinaya/dashboard.php', 'r', encoding='utf-8') as f:
    dash = f.read()

dash_updated = dash.replace('<h4>My Courses</h4>\n                <p>Access your enrolled Bharatanatyam batches and learning materials.</p>\n                <a href="#">View Courses &rarr;</a>',
                            '<h4>My Courses</h4>\n                <p>Access your enrolled Bharatanatyam batches and learning materials.</p>\n                <a href="courses.php">View Courses &rarr;</a>')

# Also generic match if whitespace differs
dash_updated = re.sub(r'<h4>My Courses</h4>\s*<p>.*?</p>\s*<a href="[^"]*">View Courses &rarr;</a>',
                      '<h4>My Courses</h4>\n                <p>Access your enrolled Bharatanatyam batches and learning materials.</p>\n                <a href="courses.php">View Courses &rarr;</a>',
                      dash_updated)

with open('c:/Xamp/htdocs/abhinaya/dashboard.php', 'w', encoding='utf-8') as f:
    f.write(dash_updated)

print("Updated dashboard.php link to point to courses.php")

# Update programs.html as well
programs_html = courses_php.replace('<?php\nsession_start();\n?>', '')
programs_html = programs_html.replace("<?php if(isset($_SESSION['user_id'])): ?>", "")
programs_html = programs_html.replace("<?php endif; ?>", "")

with open('c:/Xamp/htdocs/abhinaya/programs.html', 'w', encoding='utf-8') as f:
    f.write(programs_html)

print("Updated programs.html with all courses.")
