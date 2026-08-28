import urllib.request
import re

url = 'https://abhinayaainstitute.org/the-institute/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    images = re.findall(r'<img[^>]+src=[\"\']([^\"\']+)[\"\']', html)
    institute_images = [img for img in images if 'uploads' in img and not img.endswith('.svg') and 'AIRF-Favicon' not in img and 'logo' not in img.lower()]
    institute_images = list(set(institute_images))
    print('Found', len(institute_images), 'images from The Institute page')
    
    # Read gallery.html
    with open('c:/Xamp/htdocs/abhinaya/gallery.html', 'r', encoding='utf-8') as f:
        gallery = f.read()
    
    # Find the closing </div> of gallery-grid
    parts = gallery.split('</div>\n\n<!-- Lightbox container -->')
    if len(parts) == 2:
        new_images_html = ''
        for img in institute_images:
            new_images_html += f'    <img src="{img}" onclick="openLightbox(this.src)" alt="Abhinaya Gallery Image">\n'
        
        updated_gallery = parts[0] + new_images_html + '</div>\n\n<!-- Lightbox container -->' + parts[1]
        with open('c:/Xamp/htdocs/abhinaya/gallery.html', 'w', encoding='utf-8') as f:
            f.write(updated_gallery)
        print('Updated gallery.html with new images!')
    else:
        print('Could not find injection point in gallery.html')

except Exception as e:
    print('Error:', e)
