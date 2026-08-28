import os
import glob

# Find all html and php files
files = glob.glob('c:/Xamp/htdocs/abhinaya/*.html') + glob.glob('c:/Xamp/htdocs/abhinaya/*.php')

js_block = """
<script>
document.addEventListener("DOMContentLoaded", function() {
    // Automatically add reveal class to important elements if they don't have it
    var elementsToReveal = document.querySelectorAll('h2, h3, p:not(.hero-content p):not(footer p):not(.footer-bottom p), .gallery-card, .student-card, .about-box, .course-card, img:not(nav img):not(footer img), footer');
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
"""

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check if this is a web page (has body tag)
    if '</body>' in content:
        # Check if the scroll reveal JS is already there
        if 'IntersectionObserver' not in content:
            # Inject it right before </body>
            new_content = content.replace('</body>', f'{js_block}</body>')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Injected scroll reveal script into {os.path.basename(filepath)}")

print("Done injecting scroll reveal script.")
