import os
import re

html_path = r'c:\Xamp\htdocs\abhinaya\home.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# The pattern to remove everything between <section id="gallery"> and <footer class="footer">
pattern = re.compile(r'(<section id="gallery">.*?</section>\s*<section id="students">.*?</section>\s*)(<footer class="footer">)', re.DOTALL)

new_content = """
<!-- NEW MIDDLE SECTIONS -->

<section class="content-section about-intro" style="padding: 100px 10%; text-align: center; background: rgba(0,0,0,0.4);">
    <div style="max-width: 900px; margin: auto;">
        <h2 class="section-title" style="margin-bottom: 30px;">Grace in Every Step</h2>
        <h3 style="color: #d4af37; font-family: 'Cinzel', serif; font-size: 2rem; margin-bottom: 20px;">
            Building Strong Foundations in Indian Classical Dance Tradition
        </h3>
        <p style="color: #d9d9d9; font-size: 1.1rem; line-height: 1.9; margin-bottom: 20px;">
            Abhinayaa Institute of Research and Fine Arts is a distinguished cultural institution dedicated to nurturing excellence in Indian classical dance through structured training, artistic discipline, and deep-rooted tradition. With decades of presence and credibility, the institute offers a holistic environment where students are guided not only in performance but also in understanding the cultural, theoretical, and expressive dimensions of the art form.
        </p>
        <p style="color: #d9d9d9; font-size: 1.1rem; line-height: 1.9; margin-bottom: 40px;">
            As a trusted platform for aspiring dancers, Abhinayaa brings together multiple classical traditions under one roof, shaping well-rounded artists through consistent mentorship and milestone-driven learning experiences. From foundational training to Arangetram journeys, the institute continues to cultivate a vibrant community that carries forward the values of heritage, precision, and artistic integrity with grace and purpose.
        </p>
        
        <div style="font-size: 1.3rem; font-style: italic; color: #f8d76d; border-left: 4px solid #d4af37; padding-left: 20px; text-align: left; margin-top: 50px;">
            "In every step of dance lies a story, a prayer, and a connection to something greater."
        </div>
    </div>
</section>

<section class="content-section core-values" style="padding: 80px 10%; background: rgba(255,255,255,0.02);">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px;">
        <div class="value-card" style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; border-left: 3px solid #d4af37;">
            <p style="font-size: 1.1rem; color: #fff;">Nurturing generations through dedicated classical dance education.</p>
        </div>
        <div class="value-card" style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; border-left: 3px solid #d4af37;">
            <p style="font-size: 1.1rem; color: #fff;">Guiding students through milestone performances with excellence.</p>
        </div>
        <div class="value-card" style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; border-left: 3px solid #d4af37;">
            <p style="font-size: 1.1rem; color: #fff;">Building a strong foundation rooted in tradition and discipline.</p>
        </div>
        <div class="value-card" style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; border-left: 3px solid #d4af37;">
            <p style="font-size: 1.1rem; color: #fff;">Curating impactful performances that celebrate classical dance and cultural expression.</p>
        </div>
        <div class="value-card" style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; border-left: 3px solid #d4af37;">
            <p style="font-size: 1.1rem; color: #fff;">Showcasing excellence across prestigious platforms and renowned cultural festivals.</p>
        </div>
        <div class="value-card" style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; border-left: 3px solid #d4af37;">
            <p style="font-size: 1.1rem; color: #fff;">Representing Indian classical dance on international stages with grace and authenticity.</p>
        </div>
    </div>
</section>

<section class="content-section tradition-location" style="padding: 100px 10%; text-align: center; background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1516280440614-37939bbacd81?auto=format&fit=crop&w=1200&q=80') center/cover fixed;">
    <h2 style="font-size: 3rem; color: #d4af37; font-family: 'Cinzel', serif; margin-bottom: 20px;">Rooted in Tradition, Moving with Grace</h2>
    <p style="font-size: 1.5rem; color: #ddd; margin-bottom: 10px;">Classical Dance & Cultural Education</p>
    <p style="font-size: 1.2rem; color: #aaa; margin-bottom: 30px;">Bharatanatyam, Training, Arangetrams</p>
    <div style="display: inline-block; padding: 15px 30px; border: 1px solid #d4af37; color: #d4af37; font-size: 1.2rem; border-radius: 30px;">
        <i class="fas fa-map-marker-alt" style="margin-right: 10px;"></i> Vasai, Maharashtra • Since 1996
    </div>
</section>

<section class="content-section associations" style="padding: 80px 10%; text-align: center;">
    <h2 class="section-title">Our Associations</h2>
    <div style="display: flex; justify-content: center; gap: 50px; flex-wrap: wrap; margin-top: 40px;">
        <div style="width: 200px; height: 100px; background: rgba(255,255,255,0.05); border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px dashed rgba(212,175,55,0.5); color: #888;">
            Partner Logo 1
        </div>
        <div style="width: 200px; height: 100px; background: rgba(255,255,255,0.05); border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px dashed rgba(212,175,55,0.5); color: #888;">
            Partner Logo 2
        </div>
        <div style="width: 200px; height: 100px; background: rgba(255,255,255,0.05); border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px dashed rgba(212,175,55,0.5); color: #888;">
            Partner Logo 3
        </div>
    </div>
</section>

<section class="content-section shloka" style="padding: 80px 10%; background: #0a0a0a; text-align: center;">
    <div style="max-width: 800px; margin: auto; padding: 50px; border: 1px solid rgba(212,175,55,0.3); border-radius: 20px; position: relative;">
        <h2 style="color: #d4af37; font-family: 'Cinzel', serif; font-size: 2.2rem; margin-bottom: 40px;">Dhyana Moolam Gurur Murti</h2>
        
        <div style="margin-bottom: 25px;">
            <p style="font-size: 1.4rem; color: #fff; font-style: italic;">Dhyana Moolam Gurur Murti</p>
            <p style="font-size: 1rem; color: #aaa;">The root of meditation is the form of the Guru.</p>
        </div>
        <div style="margin-bottom: 25px;">
            <p style="font-size: 1.4rem; color: #fff; font-style: italic;">Pooja Moolam Gurur Padam</p>
            <p style="font-size: 1rem; color: #aaa;">The root of worship is the feet of the Guru.</p>
        </div>
        <div style="margin-bottom: 25px;">
            <p style="font-size: 1.4rem; color: #fff; font-style: italic;">Mantra Moolam Gurur Vakyam</p>
            <p style="font-size: 1rem; color: #aaa;">The root of all mantra is the word of the Guru.</p>
        </div>
        <div style="margin-bottom: 25px;">
            <p style="font-size: 1.4rem; color: #fff; font-style: italic;">Moksha Moolam Gurur Kripa</p>
            <p style="font-size: 1rem; color: #aaa;">The root of liberation is the grace of the Guru.</p>
        </div>
        
        <div style="margin-top: 40px;">
            <a href="about.html" class="btn" style="margin: 0 10px;">About Us</a>
            <a href="registration.html" class="btn" style="margin: 0 10px;">Begin Your Journey</a>
        </div>
    </div>
</section>

<section class="content-section cta" style="padding: 100px 10%; text-align: center; background: rgba(212,175,55,0.1);">
    <h2 style="font-size: 2.5rem; color: #d4af37; font-family: 'Cinzel', serif; margin-bottom: 20px;">Experience the Art of Timeless Tradition</h2>
    <p style="font-size: 1.2rem; color: #ddd; max-width: 800px; margin: 0 auto 30px; line-height: 1.8;">
        At Abhinayaa, classical dance is shaped with precision, discipline, and grace - offering a refined space where tradition is preserved and excellence is nurtured with purpose.
    </p>
    <p style="font-size: 1.1rem; color: #aaa; margin-bottom: 40px;">
        For Inquiries, mail to: <a href="mailto:info@abhinayaainstitute.org" style="color: #d4af37; text-decoration: none;">info@abhinayaainstitute.org</a>
    </p>
    <a href="contact.php" class="btn" style="font-size: 1.2rem; padding: 15px 40px;">Reach out now</a>
</section>

"""

# Ensure we use exactly \2 to keep the footer
if pattern.search(html):
    html = pattern.sub(new_content + r'\2', html)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully updated home.html!")
else:
    print("Could not find the target sections to replace!")
