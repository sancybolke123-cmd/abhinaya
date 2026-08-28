import os

replacements = {
    'contact.html': '''    <div style="max-width: 600px; margin: auto; background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px;">
        <form>
            <div style="margin-bottom: 15px; text-align: left;">
                <label style="display:block; margin-bottom: 5px;">Name</label>
                <input type="text" style="width: 100%; padding: 10px; border-radius: 5px; background: #222; color: white; border: 1px solid #444;">
            </div>
            <div style="margin-bottom: 15px; text-align: left;">
                <label style="display:block; margin-bottom: 5px;">Email</label>
                <input type="email" style="width: 100%; padding: 10px; border-radius: 5px; background: #222; color: white; border: 1px solid #444;">
            </div>
            <div style="margin-bottom: 15px; text-align: left;">
                <label style="display:block; margin-bottom: 5px;">Message</label>
                <textarea rows="4" style="width: 100%; padding: 10px; border-radius: 5px; background: #222; color: white; border: 1px solid #444;"></textarea>
            </div>
            <button style="background: #d4af37; color: black; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; cursor: pointer;">Send Message</button>
        </form>
    </div>''',
    
    'programs.html': '''    <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;">
        <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; width: 300px;">
            <h3 style="color: #d4af37; margin-bottom: 15px;">Beginner</h3>
            <p>Fundamental adavus, mudras and basic theory.</p>
        </div>
        <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; width: 300px;">
            <h3 style="color: #d4af37; margin-bottom: 15px;">Intermediate</h3>
            <p>Complex rhythms, expressions, and short items.</p>
        </div>
        <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; width: 300px;">
            <h3 style="color: #d4af37; margin-bottom: 15px;">Advanced</h3>
            <p>Full margam preparation and Arangetram training.</p>
        </div>
    </div>''',
    
    'academic-calendar.html': '''    <div style="max-width: 800px; margin: auto; text-align: left; background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px;">
        <ul style="list-style: none; padding: 0;">
            <li style="padding: 15px 0; border-bottom: 1px solid #333;"><strong style="color: #d4af37;">August 2026</strong> - New Academic Session Begins</li>
            <li style="padding: 15px 0; border-bottom: 1px solid #333;"><strong style="color: #d4af37;">October 2026</strong> - Navratri Special Performances</li>
            <li style="padding: 15px 0; border-bottom: 1px solid #333;"><strong style="color: #d4af37;">December 2026</strong> - Mid-term Evaluations</li>
            <li style="padding: 15px 0;"><strong style="color: #d4af37;">April 2027</strong> - Annual Day &amp; Final Exams</li>
        </ul>
    </div>''',
    
    'events-workshops.html': '''    <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;">
        <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; width: 350px; text-align: left;">
            <h3 style="color: #d4af37; margin-bottom: 10px;">Abhinaya Workshop</h3>
            <p style="color: #aaa; margin-bottom: 10px;">September 15, 2026</p>
            <p>A special workshop focusing on facial expressions and emotional storytelling.</p>
        </div>
        <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; width: 350px; text-align: left;">
            <h3 style="color: #d4af37; margin-bottom: 10px;">Nattuvangam Basics</h3>
            <p style="color: #aaa; margin-bottom: 10px;">November 10, 2026</p>
            <p>Introduction to reciting syllables and wielding the cymbals for dance.</p>
        </div>
    </div>''',
    
    'student-catalogue.html': '''    <p class="placeholder-text">Detailed student directory will be published soon. Stay tuned!</p>''',
    'examinations.html': '''    <div style="max-width: 600px; margin: auto; background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px;"><p>Theory and practical examinations are held annually in April. Students must maintain 80% attendance to qualify.</p></div>''',
    'attendance.html': '''    <div style="max-width: 600px; margin: auto; background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px;"><p>Students can check their monthly attendance records here once the portal is live.</p></div>''',
    'results.html': '''    <div style="max-width: 600px; margin: auto; background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px;"><p>Examination results for the academic year 2025-26 have been announced. Please contact the administration.</p></div>''',
    'certificates.html': '''    <div style="max-width: 600px; margin: auto; background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px;"><p>Digital certificates for completed courses and workshops will be available for download here.</p></div>''',
    'scholarships.html': '''    <div style="max-width: 600px; margin: auto; background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px;"><p>Abhinaya Institute offers merit-based scholarships for advanced students. Applications open in July.</p></div>'''
}

target_str = '    <p class="placeholder-text">This section is coming soon.</p>'

for filename, content in replacements.items():
    filepath = os.path.join('c:\\\\Xamp\\\\htdocs\\\\abhinaya', filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        if target_str in text:
            text = text.replace(target_str, content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f'Updated {filename}')
