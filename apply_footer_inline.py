import glob
import re

new_footer = """<footer class="footer" style="background: #5b180f; padding: 50px 8% 20px;">
    <div class="footer-container" style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 40px;">
        <div class="footer-left" style="text-align: left;">
            <img src="https://abhinayaainstitute.org/wp-content/uploads/2025/10/AIRF-Favicon.png" alt="AIRF Logo" style="width: 50px; margin-bottom: 15px;">
            <h2 style="font-family: 'Cinzel', serif; font-size: 2rem; color: white; margin: 0;">Art. Discipline. Devotion.</h2>
        </div>
        <div class="footer-links" style="display: flex; gap: 80px; text-align: left;">
            <div style="display: flex; flex-direction: column; gap: 12px;">
                <a href="home.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">Home</a>
                <a href="about.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">About</a>
                <a href="guru.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">Our Guru</a>
                <a href="core-team.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">Core Team</a>
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px;">
                <a href="gallery.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">Gallery</a>
                <a href="events-workshops.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">Events</a>
                <a href="contact.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">Contact</a>
                <a href="examinations.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">Examinations</a>
            </div>
        </div>
    </div>
    <div class="footer-bottom" style="display: flex; justify-content: space-between; align-items: center; margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 20px;">
        <p style="color: white; margin: 0; font-size: 0.9rem;">&copy;2026 AIRF. All rights reserved.</p>
        <div class="social-icons" style="display: flex; gap: 15px;">
            <a href="#" style="width: 35px; height: 35px; border-radius: 50%; background: white; color: #5b180f; display: flex; align-items: center; justify-content: center; text-decoration: none; font-size: 1.1rem;"><i class="fab fa-instagram"></i></a>
            <a href="#" style="width: 35px; height: 35px; border-radius: 50%; background: white; color: #5b180f; display: flex; align-items: center; justify-content: center; text-decoration: none; font-size: 1.1rem;"><i class="fab fa-facebook-f"></i></a>
            <a href="#" style="width: 35px; height: 35px; border-radius: 50%; background: white; color: #5b180f; display: flex; align-items: center; justify-content: center; text-decoration: none; font-size: 1.1rem;"><i class="fab fa-youtube"></i></a>
            <a href="#" style="width: 35px; height: 35px; border-radius: 50%; background: white; color: #5b180f; display: flex; align-items: center; justify-content: center; text-decoration: none; font-size: 1.1rem;"><i class="fas fa-chevron-up"></i></a>
        </div>
    </div>
</footer>"""

files = glob.glob('*.html') + glob.glob('*.php')
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = re.compile(r'<footer[^>]*>.*?</footer>', re.DOTALL | re.IGNORECASE)
    if pattern.search(content):
        new_content = pattern.sub(new_footer, content)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filepath}")
