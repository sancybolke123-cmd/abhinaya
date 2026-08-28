import re

with open('c:/Xamp/htdocs/abhinaya/home.html', 'r', encoding='utf-8') as f:
    home = f.read()

nav_match = re.search(r'<nav>.*?</nav>', home, re.DOTALL)
footer_match = re.search(r'<footer[^>]*>.*?</footer>', home, re.DOTALL)

nav_html = nav_match.group(0) if nav_match else ''
footer_html = footer_match.group(0) if footer_match else ''

contact_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reach out today - Abhinaya Institute of Research & Fine Arts</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; }}
        body {{ font-family: 'Poppins', sans-serif; background:#0a0a0a; color: white; overflow-x: hidden; }}
        body::before {{ content: ''; position: fixed; width: 400px; height: 400px; background: #d4af37; border-radius: 50%; filter: blur(180px); top: -150px; left: -100px; opacity: 0.20; z-index: -1; }}
        body::after {{ content: ''; position: fixed; width: 350px; height: 350px; background: #8b0000; border-radius: 50%; filter: blur(180px); right: -100px; bottom: -100px; opacity: 0.15; z-index: -1; }}
        
        nav {{ position: fixed; top: 0; width: 100%; display: flex; justify-content: space-between; align-items: center; padding: 20px 70px; background: rgba(0, 0, 0, 0.25); backdrop-filter: blur(15px); z-index: 999; }}
        .logo {{ display: flex; align-items: center; font-family: 'Cinzel', serif; font-size: 1.5rem; font-weight: 700; color: #d4af37; text-decoration: none; }}
        nav ul {{ display: flex; gap: 30px; list-style: none; align-items: center; }}
        nav ul li a {{ color: white; text-decoration: none; transition: 0.3s; font-weight: 500; }}
        nav ul li a:hover {{ color: #d4af37; }}
        .dropdown {{ position: relative; }}
        .dropdown-content {{ display: none; position: absolute; background: rgba(10, 10, 10, 0.95); min-width: 200px; box-shadow: 0 8px 16px rgba(0,0,0,0.5); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 10px; overflow: hidden; top: 100%; left: 0; z-index: 1000; }}
        .dropdown-content a {{ color: white; padding: 12px 16px; text-decoration: none; display: block; border-bottom: 1px solid rgba(255,255,255,0.05); transition: 0.3s; }}
        .dropdown-content a:hover {{ background-color: rgba(212, 175, 55, 0.1); color: #d4af37; }}
        .dropdown:hover .dropdown-content {{ display: block; }}
        
        .hero {{ height: 60vh; min-height: 500px; display: flex; align-items: center; justify-content: flex-start; text-align: left; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.8)), url('https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Contact-Banner.jpg') center/cover; padding: 0 10%; padding-top: 80px; }}
        .hero-content h1 {{ font-family: 'Cinzel', serif; font-size: 5rem; color: #d4af37; margin-bottom: 20px; text-shadow: 2px 2px 10px rgba(0,0,0,0.8); }}
        .hero-content p {{ font-size: 1.4rem; color: #ddd; margin-bottom: 30px; max-width: 600px; }}
        
        .content-section {{ padding: 100px 10%; display: flex; flex-wrap: wrap; gap: 60px; }}
        .contact-left {{ flex: 1.5; min-width: 300px; }}
        .contact-right {{ flex: 1; min-width: 300px; }}
        
        .section-title {{ font-family: 'Cinzel', serif; color: #d4af37; font-size: 3rem; margin-bottom: 20px; }}
        .contact-desc {{ font-size: 1.1rem; color: #ccc; line-height: 1.8; margin-bottom: 40px; }}
        
        .contact-group {{ margin-bottom: 40px; padding-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        .contact-group:last-child {{ border-bottom: none; }}
        .contact-group h4 {{ color: #f8d76d; font-size: 1.2rem; margin-bottom: 15px; font-weight: 500; letter-spacing: 1px; }}
        .contact-item {{ display: flex; align-items: center; gap: 15px; margin-bottom: 10px; }}
        .contact-item i {{ color: #d4af37; font-size: 1.5rem; width: 30px; text-align: center; }}
        .contact-item a {{ color: white; text-decoration: none; font-size: 1.1rem; transition: color 0.3s; }}
        .contact-item a:hover {{ color: #d4af37; text-decoration: underline; }}
        
        .location-card {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(212,175,55,0.2); padding: 30px; border-radius: 15px; margin-bottom: 20px; border-left: 4px solid #d4af37; transition: transform 0.3s; }}
        .location-card:hover {{ transform: translateY(-5px); background: rgba(212,175,55,0.05); }}
        .location-card h3 {{ font-family: 'Cinzel', serif; color: white; font-size: 1.5rem; margin-bottom: 15px; }}
        .location-card p {{ color: #bbb; line-height: 1.6; margin-bottom: 20px; font-size: 1rem; }}
        
        .btn-outline {{ display: inline-block; padding: 10px 25px; border: 2px solid #d4af37; color: #d4af37; text-decoration: none; border-radius: 30px; font-weight: 500; transition: 0.3s; }}
        .btn-outline:hover {{ background: #d4af37; color: black; }}
        
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
        <h1>Contact Us</h1>
        <p>Reach us for inquiries and collaborations.</p>
    </div>
</section>

<section class="content-section">
    <div class="contact-left reveal-left">
        <h6 style="color: #ccc; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px;">Contact Info</h6>
        <h2 class="section-title">Start Your Journey With Us</h2>
        <p class="contact-desc">Reach out to Abhinayaa Institute for admissions, events, and collaborations. We're here to support your journey in fine arts with clarity, care, and guidance.</p>
        
        <div class="contact-group">
            <h4>For General Enquiries:</h4>
            <div class="contact-item">
                <i class="fa fa-envelope"></i>
                <a href="mailto:info@abhinayaainstitute.org">info@abhinayaainstitute.org</a>
            </div>
            <div class="contact-item">
                <i class="fa fa-phone"></i>
                <a href="tel:+918600182845">+918600182845</a>
            </div>
        </div>
        
        <div class="contact-group">
            <h4>For Course Information, Admissions and Batch Enquiries:</h4>
            <div class="contact-item">
                <i class="fa fa-envelope"></i>
                <a href="mailto:admissions@abhinayaainstitute.org">admissions@abhinayaainstitute.org</a>
            </div>
            <div class="contact-item">
                <i class="fa fa-phone"></i>
                <a href="tel:+918600173187">+918600173187</a>
            </div>
        </div>
        
        <div class="contact-group">
            <h4>For community outreach, collaborations and charitable initiatives:</h4>
            <div class="contact-item">
                <i class="fa fa-envelope"></i>
                <a href="mailto:ngo@abhinayaainstitute.org">ngo@abhinayaainstitute.org</a>
            </div>
        </div>
    </div>
    
    <div class="contact-right reveal-right">
        <h6 style="color: #ccc; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px;">Locations</h6>
        
        <div class="location-card">
            <h3>MUMBAI (HQ)</h3>
            <p>No. 1,2,3,4, Empress Tower,<br>
            Bhabhola Chulna Road, Agarwal<br>
            Heritage City, Vasai West – 401202<br>
            Mumbai, Maharashtra</p>
            <a href="https://maps.app.goo.gl/Z2fnqpTALehHWVcV6" target="_blank" class="btn-outline"><i class="fa fa-map-marker"></i> Get Directions</a>
        </div>
        
        <div class="location-card">
            <h3>BENGALURU</h3>
            <p>Rohan Upavan, Kyalasanahalli,<br>
            Near SSR College, Byrathi, Off-Hennur Road,<br>
            Kothanur Post – 560077<br>
            Bengaluru, Karnataka</p>
            <a href="https://maps.app.goo.gl/zTBG3AcwqqeCN6SKA" target="_blank" class="btn-outline"><i class="fa fa-map-marker"></i> Get Directions</a>
        </div>
        
        <div class="location-card">
            <h3>KOCHI</h3>
            <p>Pallakat Building, 1st floor,<br>
            Kannangulangara,<br>
            Tripunithura – 682306<br>
            Kochi, Kerala</p>
            <a href="https://maps.app.goo.gl/aL6eczVpEFCm2ypS7" target="_blank" class="btn-outline"><i class="fa fa-map-marker"></i> Get Directions</a>
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

with open('c:/Xamp/htdocs/abhinaya/contact.html', 'w', encoding='utf-8') as f:
    f.write(contact_html)

# Also update contact.php just in case it's used
with open('c:/Xamp/htdocs/abhinaya/contact.php', 'w', encoding='utf-8') as f:
    f.write(contact_html)

print("Successfully created contact.html and contact.php")
