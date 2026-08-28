import re

with open('c:/Xamp/htdocs/abhinaya/home.html', 'r', encoding='utf-8') as f:
    home = f.read()

nav_match = re.search(r'<nav>.*?</nav>', home, re.DOTALL)
footer_match = re.search(r'<footer[^>]*>.*?</footer>', home, re.DOTALL)

nav_html = nav_match.group(0) if nav_match else ''
nav_html = nav_html.replace('student-portal.html', 'student-portal.php')
footer_html = footer_match.group(0) if footer_match else ''

schedule_php = f"""<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Schedule - Abhinaya Institute</title>
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
            height: 40vh;
            min-height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.8)), url('images/slide1.jpg.jpg') center/cover;
            padding-top: 80px;
        }}
        .hero-content h1 {{
            font-family: 'Cinzel', serif;
            font-size: 3.5rem;
            color: #d4af37;
            margin-bottom: 10px;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
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
        <h1 class="page-title">Attendance & Schedule</h1>
    </div>
</section>

<section style="padding: 90px 10%; max-width: 800px; margin: auto; text-align: center;">
    <div class="about-box reveal" style="background: rgba(255,255,255,0.05); backdrop-filter: blur(15px); padding: 50px 40px; border-radius: 25px; border: 1px solid rgba(212,175,55,0.25); box-shadow: 0 15px 35px rgba(0,0,0,0.5);">
        <div style="width: 90px; height: 90px; margin: 0 auto 25px; background: rgba(212,175,55,0.1); border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(212,175,55,0.3);">
            <i class="fa fa-calendar-times-o" style="font-size: 2.8rem; color: #d4af37;"></i>
        </div>
        
        <h2 style="font-family: 'Cinzel', serif; font-size: 2.2rem; color: #d4af37; margin-bottom: 15px;">No Schedule is Set</h2>
        <p style="color: #ccc; font-size: 1.1rem; line-height: 1.8; max-width: 550px; margin: 0 auto 30px;">
            Your batch schedule and monthly attendance records have not been configured yet by the administration. Please check back soon or consult with your guru.
        </p>
        
        <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
            <?php if(isset($_SESSION['user_id'])): ?>
                <a href="dashboard.php" style="display: inline-block; background: linear-gradient(135deg, #d4af37, #f8d76d); color: black; padding: 12px 30px; border-radius: 50px; text-decoration: none; font-weight: 600; transition: 0.3s;"><i class="fa fa-arrow-left"></i> Back to Dashboard</a>
            <?php endif; ?>
            <a href="ACADEMIC CALENDAR.pdf" target="_blank" style="display: inline-block; background: transparent; border: 2px solid #d4af37; color: #d4af37; padding: 12px 30px; border-radius: 50px; text-decoration: none; font-weight: 600; transition: 0.3s;"><i class="fa fa-calendar"></i> Academic Calendar</a>
        </div>
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

with open('c:/Xamp/htdocs/abhinaya/schedule.php', 'w', encoding='utf-8') as f:
    f.write(schedule_php)

print("Created schedule.php")

# Update dashboard.php link
with open('c:/Xamp/htdocs/abhinaya/dashboard.php', 'r', encoding='utf-8') as f:
    dash = f.read()

dash_updated = re.sub(r'<h4>Attendance</h4>\s*<p>.*?</p>\s*<a href="[^"]*">View Schedule &rarr;</a>',
                      '<h4>Attendance</h4>\n                <p>Check your monthly class attendance and upcoming schedules.</p>\n                <a href="schedule.php">View Schedule &rarr;</a>',
                      dash)

with open('c:/Xamp/htdocs/abhinaya/dashboard.php', 'w', encoding='utf-8') as f:
    f.write(dash_updated)

print("Updated dashboard.php Attendance link to schedule.php")
