import os
import glob
import re

base_dir = 'c:/Xamp/htdocs/abhinaya'

# 1. Update Navigation Links in all HTML/PHP files
google_form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSeoto6_5Cs139HBzN0_7P20A8oqpkJ3sCaSuMCh--0_UjTdkQ/viewform?usp=dialog" target="_blank'

files = glob.glob(os.path.join(base_dir, '*.html')) + glob.glob(os.path.join(base_dir, '*.php'))
for filepath in files:
    if os.path.basename(filepath) in ['admission.php', 'create_table.php', 'db.php', 'alter_table.php', 'setup.php']:
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace href="admission.php" with the google form url
    new_content = content.replace('href="admission.php"', f'href="{google_form_url}"')
    
    # Also change the menu "Contact" to "contact.php" if it was "contact.html"
    new_content = new_content.replace('href="contact.html"', 'href="contact.php"')
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated nav links in {os.path.basename(filepath)}")

# 2. Delete admission.php
try:
    os.remove(os.path.join(base_dir, 'admission.php'))
    print("Deleted admission.php")
except OSError:
    pass

# 3. Create fee-payment.php
fee_payment_php = """<?php
require 'db.php';

$message = "";
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $full_name = mysqli_real_escape_string($conn, $_POST['full_name']);
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $course = mysqli_real_escape_string($conn, $_POST['course']);
    
    $payment_receipt = "";
    if (isset($_FILES['payment_receipt']) && $_FILES['payment_receipt']['error'] == 0) {
        $target_dir = "uploads/";
        if (!is_dir($target_dir)) {
            mkdir($target_dir, 0777, true);
        }
        $payment_receipt = $target_dir . time() . "_" . basename($_FILES["payment_receipt"]["name"]);
        move_uploaded_file($_FILES["payment_receipt"]["tmp_name"], $payment_receipt);
    }

    $sql = "INSERT INTO payments (full_name, email, course, payment_receipt) 
            VALUES ('$full_name', '$email', '$course', '$payment_receipt')";

    if (mysqli_query($conn, $sql)) {
        $message = "<p style='color: #4CAF50; text-align: center; margin-bottom: 20px; font-weight: bold;'>Payment receipt submitted successfully! We will verify it shortly.</p>";
    } else {
        $message = "<p style='color: red; text-align: center; margin-bottom: 20px;'>Error submitting payment: " . mysqli_error($conn) . "</p>";
    }
}
?>
"""

with open(os.path.join(base_dir, 'template.html'), 'r', encoding='utf-8') as f:
    template = f.read()

# Split template at content-section
head_nav = template.split('<section class="hero"')[0]
footer = '<footer class="footer">' + template.split('<footer class="footer">')[1]

fee_html = head_nav + """
<section class="hero" style="height: 40vh; min-height: 300px;">
    <div class="hero-content">
        <h1 class="page-title" style="font-size: 3.5rem;">Fee Payment</h1>
    </div>
</section>
<section class="form-section" style="padding: 100px 10%; max-width: 800px; margin: auto;">
    <h2 class="section-title" style="text-align:center; font-size:3rem; font-family:'Cinzel',serif; color:#d4af37; margin-bottom:25px;">Upload Payment Receipt</h2>
    <?php echo $message; ?>
    <div class="form-container" style="background:rgba(255,255,255,.05); backdrop-filter:blur(10px); padding:40px; border-radius:25px; border:1px solid rgba(212,175,55,0.2);">
        <form action="fee-payment.php" method="POST" enctype="multipart/form-data">
            <div class="form-group" style="margin-bottom: 20px;">
                <label for="full_name" style="display: block; margin-bottom: 8px; color: #ddd;">Full Name *</label>
                <input type="text" id="full_name" name="full_name" required style="width: 100%; padding: 12px; background: rgba(0,0,0,0.5); border: 1px solid rgba(212,175,55,0.5); color: white; border-radius: 8px; font-family: 'Poppins', sans-serif;">
            </div>
            <div class="form-group" style="margin-bottom: 20px;">
                <label for="email" style="display: block; margin-bottom: 8px; color: #ddd;">Email Address *</label>
                <input type="email" id="email" name="email" required style="width: 100%; padding: 12px; background: rgba(0,0,0,0.5); border: 1px solid rgba(212,175,55,0.5); color: white; border-radius: 8px; font-family: 'Poppins', sans-serif;">
            </div>
            <div class="form-group" style="margin-bottom: 20px;">
                <label for="course" style="display: block; margin-bottom: 8px; color: #ddd;">Course Enrolled *</label>
                <select id="course" name="course" required style="width: 100%; padding: 12px; background: rgba(0,0,0,0.5); border: 1px solid rgba(212,175,55,0.5); color: white; border-radius: 8px; font-family: 'Poppins', sans-serif;">
                    <option value="">Select a course</option>
                    <option value="Beginner Course">Beginner Course</option>
                    <option value="Intermediate Course">Intermediate Course</option>
                    <option value="Advanced Training">Advanced Training</option>
                </select>
            </div>
            <div class="form-group" style="margin-bottom: 20px;">
                <label for="payment_receipt" style="display: block; margin-bottom: 8px; color: #ddd;">Payment Receipt (Upload Screenshot) *</label>
                <p style="font-size: 0.9rem; color: #aaa; margin-bottom: 5px;">Please transfer the admission fee via UPI and upload the successful transaction screenshot here.</p>
                <input type="file" id="payment_receipt" name="payment_receipt" accept="image/*,application/pdf" required style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(212,175,55,0.5); color: white; border-radius: 8px;">
            </div>
            <button type="submit" class="btn-submit" style="width: 100%; padding: 15px; background: linear-gradient(135deg, #d4af37, #f8d76d); color: black; font-weight: 600; border: none; border-radius: 50px; cursor: pointer; transition: 0.4s; font-family: 'Poppins', sans-serif; font-size: 1.1rem; margin-top: 10px;">Submit Payment Receipt</button>
        </form>
    </div>
</section>
""" + footer

with open(os.path.join(base_dir, 'fee-payment.php'), 'w', encoding='utf-8') as f:
    f.write(fee_payment_php + fee_html)
print("Created fee-payment.php")
try:
    os.remove(os.path.join(base_dir, 'fee-payment.html'))
    print("Deleted fee-payment.html")
except OSError:
    pass

# 4. Create contact.php
contact_php = """<?php
require 'db.php';
$message = "";
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = mysqli_real_escape_string($conn, $_POST['name']);
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $query = mysqli_real_escape_string($conn, $_POST['query']);
    
    $sql = "INSERT INTO contacts (name, email, query) VALUES ('$name', '$email', '$query')";
    if (mysqli_query($conn, $sql)) {
        $message = "<p style='color: #4CAF50; text-align: center; margin-bottom: 20px; font-weight: bold;'>Thank you! Your message has been sent.</p>";
    } else {
        $message = "<p style='color: red; text-align: center; margin-bottom: 20px;'>Error: " . mysqli_error($conn) . "</p>";
    }
}
?>
"""
contact_html = head_nav + """
<section class="hero" style="height: 40vh; min-height: 300px;">
    <div class="hero-content">
        <h1 class="page-title" style="font-size: 3.5rem;">Contact Us</h1>
    </div>
</section>
<section class="form-section" style="padding: 100px 10%; max-width: 800px; margin: auto;">
    <h2 class="section-title" style="text-align:center; font-size:3rem; font-family:'Cinzel',serif; color:#d4af37; margin-bottom:25px;">Get In Touch</h2>
    <?php echo $message; ?>
    <div class="form-container" style="background:rgba(255,255,255,.05); backdrop-filter:blur(10px); padding:40px; border-radius:25px; border:1px solid rgba(212,175,55,0.2);">
        <form action="contact.php" method="POST">
            <div class="form-group" style="margin-bottom: 20px;">
                <label for="name" style="display: block; margin-bottom: 8px; color: #ddd;">Your Name *</label>
                <input type="text" id="name" name="name" required style="width: 100%; padding: 12px; background: rgba(0,0,0,0.5); border: 1px solid rgba(212,175,55,0.5); color: white; border-radius: 8px; font-family: 'Poppins', sans-serif;">
            </div>
            <div class="form-group" style="margin-bottom: 20px;">
                <label for="email" style="display: block; margin-bottom: 8px; color: #ddd;">Email Address *</label>
                <input type="email" id="email" name="email" required style="width: 100%; padding: 12px; background: rgba(0,0,0,0.5); border: 1px solid rgba(212,175,55,0.5); color: white; border-radius: 8px; font-family: 'Poppins', sans-serif;">
            </div>
            <div class="form-group" style="margin-bottom: 20px;">
                <label for="query" style="display: block; margin-bottom: 8px; color: #ddd;">Your Message *</label>
                <textarea id="query" name="query" rows="5" required style="width: 100%; padding: 12px; background: rgba(0,0,0,0.5); border: 1px solid rgba(212,175,55,0.5); color: white; border-radius: 8px; font-family: 'Poppins', sans-serif;"></textarea>
            </div>
            <button type="submit" class="btn-submit" style="width: 100%; padding: 15px; background: linear-gradient(135deg, #d4af37, #f8d76d); color: black; font-weight: 600; border: none; border-radius: 50px; cursor: pointer; transition: 0.4s; font-family: 'Poppins', sans-serif; font-size: 1.1rem; margin-top: 10px;">Send Message</button>
        </form>
    </div>
</section>
""" + footer

with open(os.path.join(base_dir, 'contact.php'), 'w', encoding='utf-8') as f:
    f.write(contact_php + contact_html)
print("Created contact.php")
try:
    os.remove(os.path.join(base_dir, 'contact.html'))
    print("Deleted contact.html")
except OSError:
    pass


# 5. Populate the static HTML pages with stunning generic content

pages_content = {
    "student-catalogue.html": ('Student Catalogue', 'Explore our comprehensive list of students and alumni who have graced the stage with their devotion to Bharatanatyam.'),
    "academic-calendar.html": ('Academic Calendar', 'Stay updated with our yearly schedule, examination dates, holidays, and cultural events.'),
    "examinations.html": ('Examinations', 'Details regarding the grading system, practical and theory exam dates, and syllabus requirements.'),
    "attendance.html": ('Attendance', 'Minimum 85% attendance is required to qualify for annual examinations and stage performances. Discipline is key.'),
    "results.html": ('Results', 'View the latest results for beginner, intermediate, and advanced batch examinations.'),
    "certificates.html": ('Certificates', 'Information on the diploma and certification processes awarded upon completion of Arangetram.'),
    "events-workshops.html": ('Events & Workshops', 'Join our upcoming intensive workshops, guest lectures by renowned gurus, and our grand annual day celebration.'),
    "scholarships.html": ('Scholarships', 'We offer merit-based scholarships to exceptionally talented and dedicated students to nurture their classical journey.'),
    "programs.html": ('Our Programs', 'Discover our structured courses tailored for beginners, intermediates, and advanced professional dancers.')
}

for filename, (title, desc) in pages_content.items():
    html_content = head_nav + f"""
    <section class="hero" style="height: 40vh; min-height: 300px; background: linear-gradient(rgba(0,0,0,.7),rgba(0,0,0,.7)), url('https://images.unsplash.com/photo-1516280440614-37939bbacd81?auto=format&fit=crop&w=1200&q=80') center/cover;">
        <div class="hero-content">
            <h1 class="page-title" style="font-size: 3.5rem; color: #d4af37; font-family: 'Cinzel', serif;">{title}</h1>
        </div>
    </section>
    
    <section class="content-section" style="min-height: 40vh; padding: 100px 10%;">
        <div class="about-box" style="background:rgba(255,255,255,.05); backdrop-filter:blur(10px); padding:40px; border-radius:25px; border:1px solid rgba(212,175,55,0.2); text-align: center; max-width: 900px; margin: auto;">
            <h2 style="color: #d4af37; font-family: 'Cinzel', serif; margin-bottom: 20px;">{title}</h2>
            <p style="color: #ddd; font-size: 1.1rem; line-height: 1.8;">{desc}</p>
            <div style="margin-top: 40px; border-top: 1px solid rgba(212,175,55,0.2); padding-top: 30px;">
                <p style="color: #aaa; font-style: italic;">Detailed information will be updated shortly by the administration.</p>
            </div>
        </div>
    </section>
    """ + footer
    
    with open(os.path.join(base_dir, filename), 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Updated {filename}")

# 6. Update setup.php to include the new tables
setup_path = os.path.join(base_dir, 'setup.php')
with open(setup_path, 'r', encoding='utf-8') as f:
    setup_content = f.read()

new_tables = """
// Create payments table
$sql = "CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    course VARCHAR(100) NOT NULL,
    payment_receipt VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)";
mysqli_query($conn, $sql);

// Create contacts table
$sql = "CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    query TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)";
mysqli_query($conn, $sql);
"""
if "payments" not in setup_content:
    setup_content = setup_content.replace('// Add payment_receipt column if not exists', new_tables + '\n// Add payment_receipt column if not exists')
    with open(setup_path, 'w', encoding='utf-8') as f:
        f.write(setup_content)
    print("Updated setup.php with payments and contacts tables.")

print("All frontend updates complete.")
