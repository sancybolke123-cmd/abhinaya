import glob
import os
import re

directory = 'c:/Xamp/htdocs/abhinaya'
files = glob.glob(os.path.join(directory, '*.html')) + glob.glob(os.path.join(directory, '*.php'))

new_css = '''
<style>
/* Global Load Animation */
@keyframes fadeInScale {
    0% { opacity: 0; transform: scale(0.95); }
    100% { opacity: 1; transform: scale(1); }
}
.hero-content h1 {
    animation: fadeInScale 1.2s ease-out forwards;
}
.hero-content p {
    animation: fadeInScale 1.5s ease-out forwards;
}

/* Scroll Reveal Animations */
.reveal {
    opacity: 0;
    transform: translateY(40px);
    transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}
.reveal.active {
    opacity: 1;
    transform: translateY(0);
}
.reveal-left {
    opacity: 0;
    transform: translateX(-50px);
    transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}
.reveal-left.active {
    opacity: 1;
    transform: translateX(0);
}
.reveal-right {
    opacity: 0;
    transform: translateX(50px);
    transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}
.reveal-right.active {
    opacity: 1;
    transform: translateX(0);
}
</style>
'''

new_js = '''
<script>
document.addEventListener("DOMContentLoaded", function() {
    // Automatically add reveal class to important elements if they don't have it
    var elementsToReveal = document.querySelectorAll('h2, h3, p:not(.hero-content p):not(footer p):not(.footer-bottom p), .gallery-card, .student-card, .about-box, .course-card, img:not(nav img):not(footer img)');
    elementsToReveal.forEach(function(el) {
        if (!el.classList.contains('reveal') && !el.classList.contains('reveal-left') && !el.classList.contains('reveal-right') && !el.closest('.hero')) {
            el.classList.add('reveal');
        }
    });

    var reveals = document.querySelectorAll(".reveal, .reveal-left, .reveal-right");
    var observer = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("active");
                observer.unobserve(entry.target);
            }
        });
    }, { rootMargin: "0px 0px -30px 0px" });
    
    reveals.forEach(function(reveal) {
        observer.observe(reveal);
    });
});
</script>
'''

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # Remove old CSS and JS to avoid duplication
    content = re.sub(r'<style>\s*/\*\s*Scroll Reveal Animations.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script>\s*document\.addEventListener\("DOMContentLoaded", function\(\) {\s*var reveals = document\.querySelectorAll.*?<\/script>', '', content, flags=re.DOTALL)

    # Re-inject CSS
    if '</head>' in content:
        content = content.replace('</head>', new_css + '\n</head>')
        modified = True

    # Re-inject JS
    if '</body>' in content:
        content = content.replace('</body>', new_js + '\n</body>')
        modified = True

    if modified:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Updated animations in', file)
