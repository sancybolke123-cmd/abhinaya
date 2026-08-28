import re

with open('c:/Xamp/htdocs/abhinaya/guru.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace Hero background
content = content.replace("url('images/slide1.jpg.jpg')", "url('https://abhinayaainstitute.org/wp-content/uploads/2026/03/AIRF-Gallery-8-1536x1023.png')")

# 2. Replace left image
content = content.replace('<img src="images/slide1.jpg.jpg" alt="Our Guru">', '<img src="https://abhinayaainstitute.org/wp-content/uploads/2026/03/Guru.-Dr.-Chitra-Vishwanathan-scaled.jpg" alt="Guru Dr. Chitra Vishwanathan">')

# 3. Replace Guru text and title
old_text_block = """<h2>Guru Smita Shastry</h2>
            <p>Guru Smita Shastry is a renowned exponent of Bharatanatyam with over three decades of experience in performing, teaching, and choreographing. Her journey in classical dance is marked by a deep devotion to preserving the traditional purity of the Pandanallur style while exploring innovative thematic presentations.</p>
            <p>Under her visionary guidance, Abhinayaa Institute of Classical Bharatanatyam has flourished into a premier institution, nurturing hundreds of students to achieve excellence in art, discipline, and devotion.</p>"""

new_text_block = """<h2>Guru Dr. Chitra Vishwanathan</h2>
            <p>Guru Dr. Chitra Vishwanathan is a distinguished exponent of Bharatanatyam with over 30 years of experience in performance and pedagogy. Trained from the age of four under Guru Smt. Geeta Mahadevan and holding an MFA from Dr. Sandhya Purecha’s Bharata College of Fine Arts, Mumbai, she has been honoured with an international doctorate for her contributions to classical dance. She is renowned for her landmark Brahma Samhita choreography, extensive thematic ballets, and for training over 3000 students. Her work has represented India internationally, and she has pioneered the introduction of Manipuri dance in Palghar and Mumbai, while also being trained in Mohiniattam, Kuchipudi, and Indian folk traditions.</p>
            <p>Beyond performance, Guru Dr. Chitra Vishwanathan is deeply committed to the philosophy of teaching as a transformative journey. Her pedagogy emphasizes discipline, spiritual grounding, and emotional expression, ensuring that every student not only learns technique but also understands the deeper essence of Bharatanatyam. Through her guidance, students are nurtured into confident performers who carry forward tradition with authenticity and grace.</p>
            <p>Her choreographic work is marked by a rare ability to blend classical purity with thematic depth. From intricate solo margams to large-scale dance productions, her creations often draw from spiritual texts, cultural narratives, and contemporary interpretations, making them both relevant and timeless. Her productions are known for their visual richness, musical sensitivity, and strong narrative structure.</p>
            <p>As a cultural ambassador and mentor, she continues to shape the artistic landscape by fostering a vibrant community of dancers and learners. Through workshops, performances, and institutional initiatives, she has created platforms for aspiring artists to grow and showcase their talent. Her vision remains rooted in preserving heritage while evolving with the times, ensuring that classical arts remain meaningful for future generations.</p>"""

content = content.replace(old_text_block, new_text_block)

with open('c:/Xamp/htdocs/abhinaya/guru.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated guru.html successfully!')
