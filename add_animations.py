import glob
import re

files = glob.glob('c:/Xamp/htdocs/abhinaya/*.html')

reveal_css = '''
<style>
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

reveal_js = '''
<script>
document.addEventListener("DOMContentLoaded", function() {
    var reveals = document.querySelectorAll(".reveal, .reveal-left, .reveal-right");
    var observer = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("active");
                observer.unobserve(entry.target); // only animate once
            }
        });
    }, { rootMargin: "0px 0px -50px 0px" });
    
    reveals.forEach(function(reveal) {
        observer.observe(reveal);
    });
});
</script>
</body>
'''

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # Inject CSS
    if '/* Scroll Reveal Animations */' not in content and '</head>' in content:
        content = content.replace('</head>', reveal_css + '\n</head>')
        modified = True
        
    # Inject JS
    if 'IntersectionObserver' not in content and '</body>' in content:
        content = content.replace('</body>', reveal_js)
        modified = True

    # Add reveal classes to specific elements based on file type
    if 'gallery.html' in file:
        content = content.replace('<img src="', '<img class="reveal" src="')
        # fix double classes if any
        content = content.replace('class="reveal" class="', 'class="reveal ')
        
    if 'home.html' in file or 'about.html' in file:
        # add reveal to sections/divs
        content = re.sub(r'<div class="about-left">', '<div class="about-left reveal-left">', content)
        content = re.sub(r'<div class="about-right">', '<div class="about-right reveal-right">', content)
        content = re.sub(r'<div class="card">', '<div class="card reveal">', content)
        content = re.sub(r'<section class="gallery-section">', '<section class="gallery-section reveal">', content)
        content = re.sub(r'<div class="mission-vision">', '<div class="mission-vision reveal">', content)

    if modified or 'gallery.html' in file or 'home.html' in file or 'about.html' in file:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Added animations to', file)
