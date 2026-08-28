import re

# Read template
with open('c:/Xamp/htdocs/abhinaya/template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Extract parts
nav_match = re.search(r'<nav>.*?</nav>', template, re.DOTALL)
footer_match = re.search(r'<footer[^>]*>.*?</footer>', template, re.DOTALL)

nav_html = nav_match.group(0) if nav_match else ''
footer_html = footer_match.group(0) if footer_match else ''
head_content = template.split('</head>')[0] + '</head>'
head_content = head_content.replace('{{title}}', 'Our Guru')

# Custom CSS for Guru page
custom_css = """
<style>
.guru-container {
    display: flex;
    align-items: center;
    gap: 50px;
    margin-bottom: 80px;
    flex-wrap: wrap;
}
.guru-image-wrapper {
    flex: 1;
    min-width: 300px;
}
.guru-image-wrapper img {
    width: 100%;
    border-radius: 15px;
    box-shadow: 0 15px 30px rgba(212,175,55,0.2);
    border: 2px solid rgba(212,175,55,0.3);
}
.guru-details {
    flex: 1.5;
    min-width: 300px;
}
.guru-details h2 {
    font-family: 'Cinzel', serif;
    color: #d4af37;
    font-size: 2.5rem;
    margin-bottom: 20px;
}
.guru-details p {
    color: #ddd;
    line-height: 1.8;
    margin-bottom: 20px;
    font-size: 1.1rem;
}

/* Accordion Styles for Awards */
.awards-section h3 {
    text-align: center;
    font-family: 'Cinzel', serif;
    color: #d4af37;
    font-size: 2rem;
    margin-bottom: 40px;
}
.award-btn {
    background-color: rgba(212,175,55,0.1);
    color: white;
    cursor: pointer;
    padding: 18px;
    width: 100%;
    border: 1px solid rgba(212,175,55,0.3);
    text-align: left;
    outline: none;
    font-size: 1.2rem;
    font-family: 'Cinzel', serif;
    transition: 0.4s;
    border-radius: 8px;
    margin-bottom: 10px;
}
.award-btn.active, .award-btn:hover {
    background-color: rgba(212,175,55,0.3);
}
.award-btn:after {
    content: '\\002B';
    color: #d4af37;
    font-weight: bold;
    float: right;
    margin-left: 5px;
}
.award-btn.active:after {
    content: "\\2212";
}
.award-content {
    padding: 0 18px;
    background-color: rgba(0,0,0,0.5);
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.4s ease-out;
    border-radius: 0 0 8px 8px;
    margin-bottom: 15px;
    margin-top: -10px;
}
.award-content p {
    padding: 20px 0;
    color: #ddd;
    line-height: 1.6;
}
</style>
"""

head_content = head_content.replace('</head>', custom_css + '\n</head>')

body_html = f"""
<body>
{nav_html}

<section class="hero" style="height: 50vh; min-height: 400px; background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('images/slide1.jpg.jpg') center/cover;">
    <div class="hero-content">
        <h1 class="page-title" style="font-size: 4rem;">Our Guru</h1>
        <p>The Guiding Light of Abhinayaa Institute</p>
    </div>
</section>

<section class="content-section">
    <div class="guru-container">
        <div class="guru-image-wrapper reveal-left">
            <img src="images/slide1.jpg.jpg" alt="Our Guru">
        </div>
        <div class="guru-details reveal-right">
            <h2>Guru Smita Shastry</h2>
            <p>Guru Smita Shastry is a renowned exponent of Bharatanatyam with over three decades of experience in performing, teaching, and choreographing. Her journey in classical dance is marked by a deep devotion to preserving the traditional purity of the Pandanallur style while exploring innovative thematic presentations.</p>
            <p>Under her visionary guidance, Abhinayaa Institute of Classical Bharatanatyam has flourished into a premier institution, nurturing hundreds of students to achieve excellence in art, discipline, and devotion.</p>
        </div>
    </div>
    
    <div class="awards-section reveal">
        <h3>Awards & Recognitions</h3>
        
        <button class="award-btn">National Excellence Award (2015)</button>
        <div class="award-content">
            <p>Awarded the prestigious National Excellence Award for outstanding contribution to the promotion and preservation of Indian classical dance.</p>
        </div>
        
        <button class="award-btn">Natya Kala Ratna (2018)</button>
        <div class="award-content">
            <p>Honored with the Natya Kala Ratna title by the Cultural Heritage Academy for her innovative choreographic works that bridge traditional boundaries.</p>
        </div>
        
        <button class="award-btn">Lifetime Achievement in Arts (2022)</button>
        <div class="award-content">
            <p>Received the Lifetime Achievement Award recognizing her 30+ years of dedicated service in teaching and mentoring the next generation of dancers.</p>
        </div>
    </div>
</section>

{footer_html}

<script>
document.addEventListener("DOMContentLoaded", function() {{
    // Scroll Reveal
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
    
    // Accordion Logic
    var acc = document.querySelectorAll(".award-btn");
    var i;
    for (i = 0; i < acc.length; i++) {{
        acc[i].addEventListener("click", function() {{
            this.classList.toggle("active");
            var panel = this.nextElementSibling;
            if (panel.style.maxHeight) {{
                panel.style.maxHeight = null;
            }} else {{
                panel.style.maxHeight = panel.scrollHeight + "px";
            }}
        }});
    }}
}});
</script>

</body>
</html>
"""

full_html = head_content + body_html

with open('c:/Xamp/htdocs/abhinaya/guru.html', 'w', encoding='utf-8') as f:
    f.write(full_html)
print('Successfully rebuilt guru.html')
