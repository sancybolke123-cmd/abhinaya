import urllib.request
import re

url = 'https://abhinayaainstitute.org/gallery/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    images = re.findall(r'<img.*?src="(.*?)".*?>', html)
    # Filter for typical gallery images (usually uploads)
    gallery_images = [img for img in images if 'uploads' in img and not img.endswith('.svg') and 'AIRF-Favicon' not in img]
    gallery_images = list(set(gallery_images))
    print('Found', len(gallery_images), 'gallery images')
    for img in gallery_images:
        print(img)
except Exception as e:
    print('Error:', e)
