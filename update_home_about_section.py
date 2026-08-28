import re

with open('c:/Xamp/htdocs/abhinaya/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_section_regex = r'<section class="content-section about-intro"[^>]*>.*?<div style="max-width: 900px; margin: auto;">(.*?)</div>\s*</section>'
old_section_match = re.search(old_section_regex, content, re.DOTALL)

if old_section_match:
    inner_content = old_section_match.group(1)
    
    # We need to make the inner content left-aligned, so we'll just wrap it in a flex container
    
    # Also adjust the inner text alignment to be left
    inner_content = inner_content.replace('text-align: center;', 'text-align: left;')
    
    # The title "Grace in Every Step" might be centered via CSS class "section-title". Let's override it
    inner_content = inner_content.replace('class="section-title"', 'class="section-title" style="text-align: left; margin-bottom: 20px;"')
    
    new_section = f"""<section class="content-section about-intro" style="padding: 100px 10%; background: rgba(0,0,0,0.4);">
    <div style="display: flex; align-items: center; gap: 50px; flex-wrap: wrap; max-width: 1200px; margin: auto;">
        <div style="flex: 1; min-width: 300px;" class="reveal-left">
            <img src="https://abhinayaainstitute.org/wp-content/uploads/2026/04/AIRF-Gallery36.jpg" alt="Grace in Every Step" style="width: 100%; border-radius: 15px; box-shadow: 0 15px 30px rgba(212,175,55,0.2); border: 2px solid rgba(212,175,55,0.3);">
        </div>
        <div style="flex: 1.5; min-width: 300px; text-align: left;" class="reveal-right">
            {inner_content}
        </div>
    </div>
</section>"""

    new_content = content[:old_section_match.start()] + new_section + content[old_section_match.end():]
    
    with open('c:/Xamp/htdocs/abhinaya/home.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully updated the about-intro section in home.html")
else:
    print("Could not find the about-intro section.")
