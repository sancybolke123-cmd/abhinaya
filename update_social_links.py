import glob
import re

files = glob.glob('c:/Xamp/htdocs/abhinaya/*.html') + glob.glob('c:/Xamp/htdocs/abhinaya/*.php')

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace Instagram link
    content = content.replace('<a href="#" style="width: 35px; height: 35px; border-radius: 50%; background: white; color: #5b180f; display: flex; align-items: center; justify-content: center; text-decoration: none; font-size: 1.1rem;"><i class="fab fa-instagram"></i></a>',
                              '<a href="https://www.instagram.com/abhinayaa_dance_institute" target="_blank" style="width: 35px; height: 35px; border-radius: 50%; background: white; color: #5b180f; display: flex; align-items: center; justify-content: center; text-decoration: none; font-size: 1.1rem;"><i class="fab fa-instagram"></i></a>')

    # Replace Facebook link
    content = content.replace('<a href="#" style="width: 35px; height: 35px; border-radius: 50%; background: white; color: #5b180f; display: flex; align-items: center; justify-content: center; text-decoration: none; font-size: 1.1rem;"><i class="fab fa-facebook-f"></i></a>',
                              '<a href="https://www.facebook.com/abhinayaainstitute/" target="_blank" style="width: 35px; height: 35px; border-radius: 50%; background: white; color: #5b180f; display: flex; align-items: center; justify-content: center; text-decoration: none; font-size: 1.1rem;"><i class="fab fa-facebook-f"></i></a>')

    # Replace YouTube link
    content = content.replace('<a href="#" style="width: 35px; height: 35px; border-radius: 50%; background: white; color: #5b180f; display: flex; align-items: center; justify-content: center; text-decoration: none; font-size: 1.1rem;"><i class="fab fa-youtube"></i></a>',
                              '<a href="https://www.youtube.com/@Abhinayaa_dance_institute" target="_blank" style="width: 35px; height: 35px; border-radius: 50%; background: white; color: #5b180f; display: flex; align-items: center; justify-content: center; text-decoration: none; font-size: 1.1rem;"><i class="fab fa-youtube"></i></a>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
print("Successfully updated social media links in all files.")
