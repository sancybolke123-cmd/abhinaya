import re

with open('c:/Xamp/htdocs/abhinaya/about.html', 'r', encoding='utf-8') as f:
    text = f.read()

images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', text)
institute_images = [img for img in images if 'AIRF-Favicon' not in img]
institute_images = list(set(institute_images))
print('Found', len(institute_images), 'images from about.html')

with open('c:/Xamp/htdocs/abhinaya/gallery.html', 'r', encoding='utf-8') as f:
    gallery = f.read()

parts = gallery.split('</div>\n\n<!-- Lightbox container -->')
if len(parts) == 2:
    new_images_html = ''
    for img in institute_images:
        new_images_html += f'    <img src="{img}" onclick="openLightbox(this.src)" alt="Abhinaya Institute Image">\n'
    
    updated_gallery = parts[0] + new_images_html + '</div>\n\n<!-- Lightbox container -->' + parts[1]
    with open('c:/Xamp/htdocs/abhinaya/gallery.html', 'w', encoding='utf-8') as f:
        f.write(updated_gallery)
    print('Updated gallery.html with local about.html images!')
else:
    print('Could not find injection point.')
