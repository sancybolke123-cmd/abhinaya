import re

with open('c:/Xamp/htdocs/abhinaya/home.html', 'r', encoding='utf-8') as f:
    home = f.read()

# Extract parts
nav_match = re.search(r'<nav>.*?</nav>', home, re.DOTALL)
footer_match = re.search(r'<footer[^>]*>.*?</footer>', home, re.DOTALL)

nav_html = nav_match.group(0) if nav_match else ''
footer_html = footer_match.group(0) if footer_match else ''

# Construct about.html
about_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Institute - Abhinaya Institute</title>
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
        
        /* Dropdown Styles */
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
            height: 50vh;
            min-height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery36.jpg') center/cover;
            padding-top: 80px;
        }}
        .hero-content h1 {{
            font-family: 'Cinzel', serif;
            font-size: 4rem;
            color: #d4af37;
            margin-bottom: 20px;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
        }}
        .hero-content p {{
            font-size: 1.2rem;
            color: #ddd;
            margin-bottom: 30px;
        }}
        
        /* Content Containers */
        .content-section {{ padding: 80px 10%; }}
        .flex-container {{ display: flex; align-items: center; gap: 50px; flex-wrap: wrap; margin-bottom: 80px; }}
        .flex-container.reverse {{ flex-direction: row-reverse; }}
        .image-wrapper {{ flex: 1; min-width: 300px; }}
        .image-wrapper img {{
            width: 100%;
            border-radius: 15px;
            box-shadow: 0 15px 30px rgba(212,175,55,0.2);
            border: 2px solid rgba(212,175,55,0.3);
        }}
        .text-wrapper {{ flex: 1.5; min-width: 300px; }}
        .text-wrapper h2 {{
            font-family: 'Cinzel', serif;
            color: #d4af37;
            font-size: 2.5rem;
            margin-bottom: 20px;
        }}
        .text-wrapper p {{
            color: #ddd;
            line-height: 1.8;
            margin-bottom: 20px;
            font-size: 1.1rem;
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
    <div class="hero-content">
        <h1>The Institute</h1>
        <p>A Legacy of Classical Arts & Culture</p>
    </div>
</section>

<section class="content-section">
    <!-- First Block -->
    <div class="flex-container">
        <div class="image-wrapper reveal-left">
            <img src="https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Gallery-8-1536x1023.png" alt="Abhinaya Institute Campus">
        </div>
        <div class="text-wrapper reveal-right">
            <h2>Our Heritage & Vision</h2>
            <p>Abhinayaa Institute of Research and Fine Arts is a distinguished cultural institution dedicated to nurturing excellence in Indian classical dance through structured training, artistic discipline, and deep-rooted tradition.</p>
            <p>With decades of presence and credibility, the institute offers a holistic environment where students are guided not only in performance but also in understanding the cultural, theoretical, and expressive dimensions of the art form.</p>
        </div>
    </div>
    
    <!-- Second Block (Reversed) -->
    <div class="flex-container reverse">
        <div class="image-wrapper reveal-right">
            <img src="images/slide1.jpg.jpg" alt="Dance Performance">
        </div>
        <div class="text-wrapper reveal-left">
            <h2>A Holistic Platform</h2>
            <p>As a trusted platform for aspiring dancers, Abhinayaa brings together multiple classical traditions under one roof, shaping well-rounded artists through consistent mentorship and milestone-driven learning experiences.</p>
            <p>From foundational training to Arangetram journeys, the institute continues to cultivate a vibrant community that carries forward the values of heritage, precision, and artistic integrity with grace and purpose.</p>
        </div>
    </div>
    
    <!-- Core Values block -->
    <div class="text-center reveal" style="text-align: center; margin-top: 50px;">
        <h2 style="font-family: 'Cinzel', serif; color: #d4af37; font-size: 2.5rem; margin-bottom: 30px;">Our Core Values</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin-top: 40px;">
            <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; border-top: 3px solid #d4af37;">
                <h3 style="color: #fff; margin-bottom: 15px; font-family: 'Cinzel', serif;">Tradition</h3>
                <p style="color: #bbb; line-height: 1.6;">Rooted deeply in the Pandanallur style, we preserve the authentic heritage and rigid discipline of classical Bharatanatyam.</p>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; border-top: 3px solid #d4af37;">
                <h3 style="color: #fff; margin-bottom: 15px; font-family: 'Cinzel', serif;">Discipline</h3>
                <p style="color: #bbb; line-height: 1.6;">Instilling unwavering dedication and focus, ensuring students cultivate resilience alongside artistic expression.</p>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; border-top: 3px solid #d4af37;">
                <h3 style="color: #fff; margin-bottom: 15px; font-family: 'Cinzel', serif;">Excellence</h3>
                <p style="color: #bbb; line-height: 1.6;">Striving for perfection in technique, expression, and theoretical knowledge at every stage of the learning journey.</p>
            </div>
        </div>
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

with open('c:/Xamp/htdocs/abhinaya/about.html', 'w', encoding='utf-8') as f:
    f.write(about_html)

print("Successfully created about.html")
