import glob
import re

new_footer = """<footer class="footer">
    <div class="footer-container">
        <div class="footer-left">
            <img src="https://abhinayaainstitute.org/wp-content/uploads/2025/10/AIRF-Favicon.png" alt="AIRF Logo" class="footer-logo">
            <h2>Art. Discipline. Devotion.</h2>
        </div>
        <div class="footer-links">
            <div>
                <a href="home.html">Home</a>
                <a href="about.html">About</a>
                <a href="guru.html">Our Guru</a>
                <a href="core-team.html">Core Team</a>
            </div>
            <div>
                <a href="gallery.html">Gallery</a>
                <a href="events-workshops.html">Events</a>
                <a href="contact.html">Contact</a>
                <a href="examinations.html">Examinations</a>
            </div>
        </div>
    </div>
    <div class="footer-bottom">
        <p>&copy;2026 AIRF. All rights reserved.</p>
        <div class="social-icons">
            <a href="#"><i class="fab fa-instagram"></i></a>
            <a href="#"><i class="fab fa-facebook-f"></i></a>
            <a href="#"><i class="fab fa-youtube"></i></a>
            <a href="#"><i class="fas fa-chevron-up"></i></a>
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
