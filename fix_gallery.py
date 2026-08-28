import urllib.request
import re

# 1. Scrape original gallery images
url = 'https://abhinayaainstitute.org/gallery/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    images = re.findall(r'<img[^>]+src=[\"\']([^\"\']+)[\"\']', html)
    gallery_images = [img for img in images if 'uploads' in img and not img.endswith('.svg') and 'AIRF-Favicon' not in img and 'logo' not in img.lower()]
    gallery_images = list(set(gallery_images))
except:
    gallery_images = []

# 2. Get images from about.html
with open('c:/Xamp/htdocs/abhinaya/about.html', 'r', encoding='utf-8') as f:
    about_text = f.read()
about_imgs_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', about_text)
about_images = [img for img in about_imgs_matches if 'AIRF-Favicon' not in img]
about_images = list(set(about_images))

all_images = gallery_images + about_images

# 3. Build HTML
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

for img in all_images:
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

# 4. Inject into gallery.html
with open('c:/Xamp/htdocs/abhinaya/gallery.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace {{title}} with Gallery
text = text.replace('{{title}}', 'Gallery')

# Replace content-section with gallery_html
import re
text = re.sub(r'<section class="content-section".*?</section>', gallery_html, text, flags=re.DOTALL)

with open('c:/Xamp/htdocs/abhinaya/gallery.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed gallery.html with all images!')
