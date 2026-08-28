import re

with open('c:/Xamp/htdocs/abhinaya/home.html', 'r', encoding='utf-8') as f:
    home = f.read()

# Extract parts
nav_match = re.search(r'<nav>.*?</nav>', home, re.DOTALL)
footer_match = re.search(r'<footer[^>]*>.*?</footer>', home, re.DOTALL)

nav_html = nav_match.group(0) if nav_match else ''
footer_html = footer_match.group(0) if footer_match else ''

about_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About - Abhinaya Institute of Research & Fine Arts</title>
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
            height: 60vh;
            min-height: 500px;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            text-align: left;
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.8)), url('https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Nataraja.jpg') center/cover;
            padding: 0 10%;
            padding-top: 80px;
        }}
        .hero-content h1 {{
            font-family: 'Cinzel', serif;
            font-size: 5rem;
            color: #d4af37;
            margin-bottom: 20px;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
        }}
        .hero-content p {{
            font-size: 1.4rem;
            color: #ddd;
            margin-bottom: 30px;
            max-width: 600px;
        }}
        
        /* Content Sections */
        .content-section {{ padding: 80px 10%; }}
        .flex-container {{ display: flex; align-items: flex-start; gap: 50px; flex-wrap: wrap; margin-bottom: 80px; }}
        .text-wrapper-large {{ flex: 2; min-width: 300px; }}
        .text-wrapper-small {{ flex: 1; min-width: 250px; }}
        
        .section-title {{
            font-family: 'Cinzel', serif;
            color: #d4af37;
            font-size: 3rem;
            margin-bottom: 30px;
        }}
        .text-content p {{
            color: #ddd;
            line-height: 1.9;
            margin-bottom: 20px;
            font-size: 1.1rem;
            text-align: justify;
        }}
        
        /* Core Values & Stats */
        .chat-bubble {{
            background: rgba(255,255,255,0.05);
            padding: 25px;
            border-radius: 15px;
            border-left: 4px solid #d4af37;
            margin-bottom: 20px;
        }}
        .chat-bubble h4 {{
            color: #f8d76d;
            font-size: 1.2rem;
            margin-bottom: 10px;
        }}
        .chat-bubble p {{ color: #ccc; }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 40px;
            margin-top: 60px;
        }}
        .stat-item {{
            background: rgba(255,255,255,0.02);
            padding: 40px 20px;
            border-radius: 20px;
            text-align: center;
            border: 1px solid rgba(212,175,55,0.2);
            transition: transform 0.3s;
        }}
        .stat-item:hover {{ transform: translateY(-10px); background: rgba(212,175,55,0.05); }}
        .stat-number {{
            font-family: 'Cinzel', serif;
            font-size: 4rem;
            color: #d4af37;
            margin-bottom: 10px;
        }}
        .stat-desc {{ font-size: 1.2rem; color: #ddd; }}
        
        /* Festivals List */
        .festival-list {{
            background: #6A0A00;
            padding: 80px 10%;
        }}
        .festival-row {{
            display: flex;
            justify-content: space-between;
            padding: 20px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            color: white;
            font-size: 1.1rem;
        }}
        .festival-row:last-child {{ border-bottom: none; }}
        .festival-row h4 {{ font-weight: 500; font-family: 'Cinzel', serif; font-size: 1.2rem; color: #f8d76d; flex: 2; }}
        .festival-row div {{ flex: 1; }}
        .festival-row div.right {{ text-align: right; font-weight: bold; }}
        
        @media (max-width: 768px) {{
            .festival-row {{ flex-direction: column; gap: 10px; }}
            .festival-row div.right {{ text-align: left; }}
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
        <h1>About Us</h1>
        <p>Empowering dancers through tradition and knowledge.</p>
    </div>
</section>

<section class="content-section">
    <div class="flex-container">
        <div class="text-wrapper-small reveal-left">
            <h6 style="color: #d4af37; font-size: 1.2rem; text-transform: uppercase; letter-spacing: 2px;">Our Legacy</h6>
        </div>
        <div class="text-wrapper-large text-content reveal-right">
            <p>Abhinayaa Institute of Research and Fine Arts, founded by Guru Dr. Chitra Vishwanathan, is a distinguished 30-year-old NGO dedicated to preserving, promoting, and advancing the rich heritage of Indian classical dance. With a strong foundation rooted in tradition and a forward-looking vision, the institute has evolved into a respected cultural and educational space for aspiring artists across generations.</p>
            
            <p>With over 30 years of its presence in Vasai, Abhinayaa has become a landmark institution in the region, known for its commitment to excellence, discipline, and authenticity in training. It proudly stands as the only institute in the Palghar District recognized under the Government of Maharashtra’s GR, enabling students to receive a 25-mark grace benefit – an achievement that reflects both credibility and academic alignment. Further strengthening its stature, Abhinayaa is also the only ISO-certified dance institute in the district, upholding structured pedagogy and consistently high standards in arts education.</p>
            
            <p>The institute has nurtured and trained over 3000 students, building a vibrant community of dancers who carry forward the values of dedication, cultural pride, and artistic integrity. With more than 500 Arangetrams successfully conducted, Abhinayaa has consistently demonstrated its ability to guide students through one of the most significant milestones in a classical dancer’s journey with precision and excellence.</p>
        </div>
    </div>
    
    <div class="flex-container" style="margin-top: 60px;">
        <div class="text-wrapper-large text-content reveal-left">
            <p>Abhinayaa serves as a comprehensive platform where multiple classical dance forms are taught under one roof, offering students the opportunity to explore, specialize, and grow within a holistic artistic environment. The institute emphasizes not only performance but also theoretical understanding, cultural context, and personal discipline, ensuring well-rounded development for every learner.</p>
            <p>Driven by its enduring mission, Abhinayaa continues to nurture artistry, preserve cultural heritage, and inspire future generations. It stands as a trusted institution where tradition meets structured learning, shaping artists who embody grace, knowledge, and a deep respect for Indian classical arts.</p>
            <p>At its core, Abhinayaa is a space where passion finds direction and creativity is shaped with purpose. By fostering a culture of consistency, respect, and artistic exploration, the institute builds a meaningful connection between tradition and contemporary learners, ensuring that the spirit of classical arts remains vibrant, relevant, and deeply valued in today’s world.</p>
        </div>
        
        <div class="text-wrapper-small reveal-right">
            <h3 style="color: #d4af37; font-family: 'Cinzel', serif; font-size: 2rem; margin-bottom: 20px;">Core Values</h3>
            <div class="chat-bubble">
                <h4>Excellence & Authenticity</h4>
                <p>Upholding the highest standards while preserving the purity of classical arts.</p>
            </div>
            <div class="chat-bubble">
                <h4>Discipline & Commitment</h4>
                <p>Valuing structure, punctuality, and consistency in every aspect.</p>
            </div>
            <div class="chat-bubble">
                <h4>Integrity & Transparency</h4>
                <p>Acting with honesty, openness, and respect in all we do.</p>
            </div>
        </div>
    </div>
</section>

<section class="content-section" style="background: rgba(255,255,255,0.02); text-align: center;">
    <h2 class="section-title reveal">Our Impact & Milestones</h2>
    <div class="stats-grid">
        <div class="stat-item reveal">
            <div class="stat-number">30+</div>
            <div class="stat-desc">Years of Legacy</div>
        </div>
        <div class="stat-item reveal" style="transition-delay: 0.2s;">
            <div class="stat-number">3000+</div>
            <div class="stat-desc">Students Trained</div>
        </div>
        <div class="stat-item reveal" style="transition-delay: 0.4s;">
            <div class="stat-number">500+</div>
            <div class="stat-desc">Arangetrams Completed</div>
        </div>
    </div>
</section>

<section class="festival-list">
    <div class="flex-container">
        <div class="text-wrapper-large reveal-left">
            <h2 class="section-title" style="color: white;">Festivals Conducted in AIRF</h2>
            <p style="color: #ddd; font-size: 1.2rem; max-width: 600px;">Curating prestigious dance festivals that celebrate tradition, collaboration, and excellence across national and cultural platforms.</p>
        </div>
        <div class="text-wrapper-large reveal-right">
            <div class="festival-row">
                <h4>13 Years of Shivanjali Classical Dance Festival</h4>
                <div>Abhinayaa</div>
                <div>Annual Festival</div>
                <div class="right">2014–2026</div>
            </div>
            <div class="festival-row">
                <h4>3 Years of Banshi National Dance Festival</h4>
                <div>Abhinayaa & Gandharbi</div>
                <div>National Festival</div>
                <div class="right">2016–2018</div>
            </div>
            <div class="festival-row">
                <h4>2 Years of Guru Padmashree The Babu Singh Festival</h4>
                <div>National</div>
                <div>Dance Festival</div>
                <div class="right">2017–2018</div>
            </div>
            <div class="festival-row">
                <h4>1 Year of Nritya Lehar</h4>
                <div>Abhinayaa & Damodar</div>
                <div>Collaborative Festival</div>
                <div class="right">2018</div>
            </div>
            <div class="festival-row">
                <h4>1 Year of Rang Utsav - Krishna Ras</h4>
                <div>Abhinayaa</div>
                <div>Cultural Festival</div>
                <div class="right">2018</div>
            </div>
            <div class="festival-row">
                <h4>1 Year of Tribute to Rabindranath Tagore</h4>
                <div>Delhi Habitat</div>
                <div>Cultural Presentation</div>
                <div class="right">2017</div>
            </div>
            <div class="festival-row">
                <h4>1 Year of Children’s Dance Festival (2nd)</h4>
                <div>Abhinayaa</div>
                <div>Festival</div>
                <div class="right">2017</div>
            </div>
            <div class="festival-row">
                <h4>1 Year of Children’s National Dance Festival (1st)</h4>
                <div>Abhinayaa</div>
                <div>National Festival</div>
                <div class="right">2016</div>
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

print("Successfully recreated about.html exactly matching the source code structure!")
