import os

# Read template
with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

# Add custom styles for animated background in dashboard
custom_styles = """
    <style>
        @keyframes bgZoom {
            0% { background-size: 100%; }
            50% { background-size: 110%; }
            100% { background-size: 100%; }
        }
        body {
            background: linear-gradient(rgba(10, 10, 10, 0.75), rgba(10, 10, 10, 0.75)), url('images/Bharatanatyam Dance - Indian Dance.jpg') center/cover no-repeat fixed !important;
            animation: bgZoom 20s infinite ease-in-out;
        }
    </style>
"""
template = template.replace("</head>", custom_styles + "\n</head>")

dashboard_php_content = """<?php
session_start();
if (!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] !== true) {
    header("Location: login.html");
    exit();
}

$student_name = htmlspecialchars($_SESSION['student_name']);
$student_id = htmlspecialchars($_SESSION['student_id']);
$profile_photo = htmlspecialchars($_SESSION['profile_photo']);
$course_selection = htmlspecialchars($_SESSION['course_selection']);
$admission_status = htmlspecialchars($_SESSION['admission_status']);
?>
""" + template.replace("{{title}}", "Student Dashboard")

# Replace the content section
start_tag = '<section class="content-section"'
end_tag = '</section>'

start_idx = dashboard_php_content.find(start_tag)
end_idx = dashboard_php_content.find(end_tag, start_idx) + len(end_tag)

dashboard_html = """<section class="content-section" style="min-height: 60vh; padding: 50px 5%;">
    <div style="display: flex; gap: 30px; flex-wrap: wrap;">
        
        <!-- Sidebar / Profile Info -->
        <div style="flex: 1; min-width: 250px; max-width: 300px; background: rgba(255,255,255,0.05); padding: 30px; border-radius: 20px; text-align: center; border: 1px solid rgba(212,175,55,0.2);">
            <img src="<?php echo $profile_photo; ?>" alt="Profile Photo" style="width: 150px; height: 150px; border-radius: 50%; object-fit: cover; border: 3px solid #d4af37; margin-bottom: 20px;">
            <h3 style="color: #d4af37; font-family: 'Cinzel', serif; margin-bottom: 10px;">Welcome, <?php echo $student_name; ?></h3>
            <p style="color: #ccc; margin-bottom: 5px;"><strong>Student ID:</strong> <?php echo str_pad($student_id, 6, "0", STR_PAD_LEFT); ?></p>
            <p style="color: #ccc; margin-bottom: 5px;"><strong>Course:</strong> <?php echo $course_selection; ?></p>
            <p style="color: #ccc; margin-bottom: 20px;"><strong>Status:</strong> <span style="color: <?php echo $admission_status === 'Pending' ? '#f39c12' : '#2ecc71'; ?>;"><?php echo $admission_status; ?></span></p>
            
            <a href="logout.php" class="btn" style="width: 100%; padding: 10px; font-size: 1rem; background: rgba(255,0,0,0.2); color: #ff4d4d; border: 1px solid #ff4d4d;">
                <i class="fas fa-sign-out-alt"></i> Logout
            </a>
        </div>

        <!-- Dashboard Cards -->
        <div style="flex: 3; display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; align-content: flex-start;">
            
            <a href="ACADEMIC CALENDAR.pdf" target="_blank" style="background: rgba(255,255,255,0.05); padding: 30px 20px; border-radius: 15px; text-align: center; text-decoration: none; color: white; border: 1px solid rgba(212,175,55,0.2); transition: 0.3s;" onmouseover="this.style.background='rgba(212,175,55,0.1)'; this.style.transform='translateY(-5px)';" onmouseout="this.style.background='rgba(255,255,255,0.05)'; this.style.transform='translateY(0)';">
                <i class="fas fa-calendar-alt" style="font-size: 2.5rem; color: #d4af37; margin-bottom: 15px;"></i>
                <h4 style="font-size: 1.1rem;">Academic Calendar</h4>
            </a>
            
            <a href="#" style="background: rgba(255,255,255,0.05); padding: 30px 20px; border-radius: 15px; text-align: center; text-decoration: none; color: white; border: 1px solid rgba(212,175,55,0.2); transition: 0.3s;" onmouseover="this.style.background='rgba(212,175,55,0.1)'; this.style.transform='translateY(-5px)';" onmouseout="this.style.background='rgba(255,255,255,0.05)'; this.style.transform='translateY(0)';">
                <i class="fas fa-user-check" style="font-size: 2.5rem; color: #d4af37; margin-bottom: 15px;"></i>
                <h4 style="font-size: 1.1rem;">Attendance</h4>
            </a>
            
            <a href="#" style="background: rgba(255,255,255,0.05); padding: 30px 20px; border-radius: 15px; text-align: center; text-decoration: none; color: white; border: 1px solid rgba(212,175,55,0.2); transition: 0.3s;" onmouseover="this.style.background='rgba(212,175,55,0.1)'; this.style.transform='translateY(-5px)';" onmouseout="this.style.background='rgba(255,255,255,0.05)'; this.style.transform='translateY(0)';">
                <i class="fas fa-pen-nib" style="font-size: 2.5rem; color: #d4af37; margin-bottom: 15px;"></i>
                <h4 style="font-size: 1.1rem;">Examinations</h4>
            </a>
            
            <a href="MARKSHEET-STRUCTURE.pdf" target="_blank" style="background: rgba(255,255,255,0.05); padding: 30px 20px; border-radius: 15px; text-align: center; text-decoration: none; color: white; border: 1px solid rgba(212,175,55,0.2); transition: 0.3s;" onmouseover="this.style.background='rgba(212,175,55,0.1)'; this.style.transform='translateY(-5px)';" onmouseout="this.style.background='rgba(255,255,255,0.05)'; this.style.transform='translateY(0)';">
                <i class="fas fa-poll" style="font-size: 2.5rem; color: #d4af37; margin-bottom: 15px;"></i>
                <h4 style="font-size: 1.1rem;">Results</h4>
            </a>
            
            <a href="#" style="background: rgba(255,255,255,0.05); padding: 30px 20px; border-radius: 15px; text-align: center; text-decoration: none; color: white; border: 1px solid rgba(212,175,55,0.2); transition: 0.3s;" onmouseover="this.style.background='rgba(212,175,55,0.1)'; this.style.transform='translateY(-5px)';" onmouseout="this.style.background='rgba(255,255,255,0.05)'; this.style.transform='translateY(0)';">
                <i class="fas fa-certificate" style="font-size: 2.5rem; color: #d4af37; margin-bottom: 15px;"></i>
                <h4 style="font-size: 1.1rem;">Certificates</h4>
            </a>
            
            <a href="#" style="background: rgba(255,255,255,0.05); padding: 30px 20px; border-radius: 15px; text-align: center; text-decoration: none; color: white; border: 1px solid rgba(212,175,55,0.2); transition: 0.3s;" onmouseover="this.style.background='rgba(212,175,55,0.1)'; this.style.transform='translateY(-5px)';" onmouseout="this.style.background='rgba(255,255,255,0.05)'; this.style.transform='translateY(0)';">
                <i class="fas fa-graduation-cap" style="font-size: 2.5rem; color: #d4af37; margin-bottom: 15px;"></i>
                <h4 style="font-size: 1.1rem;">Scholarships</h4>
            </a>
            
            <a href="#" style="background: rgba(255,255,255,0.05); padding: 30px 20px; border-radius: 15px; text-align: center; text-decoration: none; color: white; border: 1px solid rgba(212,175,55,0.2); transition: 0.3s;" onmouseover="this.style.background='rgba(212,175,55,0.1)'; this.style.transform='translateY(-5px)';" onmouseout="this.style.background='rgba(255,255,255,0.05)'; this.style.transform='translateY(0)';">
                <i class="fas fa-theater-masks" style="font-size: 2.5rem; color: #d4af37; margin-bottom: 15px;"></i>
                <h4 style="font-size: 1.1rem;">Events & Workshops</h4>
            </a>
            
            <a href="The Bharatanatyam Learning Compendium.pdf" target="_blank" style="background: rgba(255,255,255,0.05); padding: 30px 20px; border-radius: 15px; text-align: center; text-decoration: none; color: white; border: 1px solid rgba(212,175,55,0.2); transition: 0.3s;" onmouseover="this.style.background='rgba(212,175,55,0.1)'; this.style.transform='translateY(-5px)';" onmouseout="this.style.background='rgba(255,255,255,0.05)'; this.style.transform='translateY(0)';">
                <i class="fas fa-book-open" style="font-size: 2.5rem; color: #d4af37; margin-bottom: 15px;"></i>
                <h4 style="font-size: 1.1rem;">Download E-book</h4>
            </a>
            
            <a href="#" style="background: rgba(255,255,255,0.05); padding: 30px 20px; border-radius: 15px; text-align: center; text-decoration: none; color: white; border: 1px solid rgba(212,175,55,0.2); transition: 0.3s; grid-column: span 1;" onmouseover="this.style.background='rgba(212,175,55,0.1)'; this.style.transform='translateY(-5px)';" onmouseout="this.style.background='rgba(255,255,255,0.05)'; this.style.transform='translateY(0)';">
                <i class="fas fa-bullhorn" style="font-size: 2.5rem; color: #d4af37; margin-bottom: 15px;"></i>
                <h4 style="font-size: 1.1rem;">Announcements</h4>
            </a>

        </div>

    </div>
</section>
"""

new_dashboard_content = dashboard_php_content[:start_idx] + dashboard_html + dashboard_php_content[end_idx:]

with open("dashboard.php", "w", encoding="utf-8") as f:
    f.write(new_dashboard_content)

print("Created dashboard.php")
