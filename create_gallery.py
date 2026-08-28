import json

images = [
"https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Gallery-7-681x1024.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Gallery-1-1024x473.png",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery28-1024x682.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Gallery-10-1024x768.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery38-1024x682.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery33-1024x682.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery23-1024x682.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery30-1024x682.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery37-1024x682.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery35-1024x682.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery29-1024x682.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Gallery-Img.png",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery26-1024x682.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery25-1024x682.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery31-1024x682.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery34-1024x682.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery36-682x1024.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Gallery-4-1024x539.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Gallery-6-830x1024.png",
"https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Gallery-2-1024x456.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery27-1024x682.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Gallery-9-1024x768.png",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery24-1024x682.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Gallery-5-1024x683.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Gallery-11-768x1024.png",
"https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Gallery-12-1024x590.png",
"https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Gallery-8-1024x682.png",
"https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Gallery-3-1024x514.jpg",
"https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery32-1024x682.jpg"
]

with open('c:/Xamp/htdocs/abhinaya/template.html', 'r', encoding='utf-8') as f:
    template = f.read()

template = template.replace('[Page Title]', 'Gallery')
template = template.replace('<title>Abhinaya Institute</title>', '<title>Gallery | Abhinaya Institute</title>')

gallery_html = '''
<style>
.gallery-grid {
    column-count: 3;
    column-gap: 15px;
    padding: 50px 10%;
    background: #0d0d0d;
}
.gallery-grid img {
    width: 100%;
    margin-bottom: 15px;
    border-radius: 10px;
    display: block;
    transition: transform 0.4s ease, box-shadow 0.4s ease;
    cursor: pointer;
}
.gallery-grid img:hover {
    transform: scale(1.03);
    box-shadow: 0 10px 20px rgba(212,175,55,0.2);
}
@media (max-width: 900px) {
    .gallery-grid {
        column-count: 2;
    }
}
@media (max-width: 600px) {
    .gallery-grid {
        column-count: 1;
    }
}
/* Modal for Lightbox */
.lightbox {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.9);
    justify-content: center;
    align-items: center;
}
.lightbox img {
    max-width: 90%;
    max-height: 90%;
    border-radius: 10px;
    box-shadow: 0 0 30px rgba(212,175,55,0.4);
}
.close-btn {
    position: absolute;
    top: 30px;
    right: 40px;
    color: white;
    font-size: 40px;
    font-weight: bold;
    cursor: pointer;
    transition: 0.3s;
}
.close-btn:hover {
    color: #d4af37;
}
</style>

<div class="gallery-grid">
'''

for img in images:
    gallery_html += f'    <img src="{img}" onclick="openLightbox(this.src)" alt="Abhinaya Gallery Image">\n'

gallery_html += '''
</div>

<!-- Lightbox container -->
<div id="lightbox" class="lightbox" onclick="closeLightbox()">
    <span class="close-btn">&times;</span>
    <img id="lightbox-img" src="">
</div>

<script>
function openLightbox(src) {
    document.getElementById("lightbox").style.display = "flex";
    document.getElementById("lightbox-img").src = src;
}
function closeLightbox() {
    document.getElementById("lightbox").style.display = "none";
}
</script>
'''

content = template.replace('<!-- [Content Section Placeholder] -->', gallery_html)

# Add font awesome if missing
if 'font-awesome' not in content:
    content = content.replace('</head>', '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">\n</head>')

with open('c:/Xamp/htdocs/abhinaya/gallery.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Generated gallery.html')
