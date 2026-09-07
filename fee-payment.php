<?php
session_start();
require 'db.php';

// Ensure payments table exists in live/cloud DB
mysqli_query($conn, "CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    course VARCHAR(100) NOT NULL,
    payment_receipt VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)");

$message = "";
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $full_name = mysqli_real_escape_string($conn, trim($_POST['full_name']));
    $email = mysqli_real_escape_string($conn, trim($_POST['email']));
    $course = mysqli_real_escape_string($conn, trim($_POST['course']));
    
    // Extract fee from course value
    preg_match('/₹(\d+)/', $course, $matches);
    $fee = isset($matches[1]) ? $matches[1] : '0';
    
    $txn_id = 'TXN' . strtoupper(uniqid());
    $date = date('Y-m-d H:i:s');
    
    $target_dir = "uploads/";
    if (!is_dir($target_dir)) {
        mkdir($target_dir, 0777, true);
    }
    
    $receipt_content = "<!DOCTYPE html>
<html>
<head>
    <title>Fee Receipt - $txn_id</title>
    <style>
        body { font-family: 'Poppins', sans-serif; background: #fafafa; padding: 40px; }
        .receipt-card { background: white; max-width: 500px; margin: auto; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 6px solid #8b0000; }
        h2 { color: #8b0000; text-align: center; margin-bottom: 5px; font-family: 'Cinzel', serif; }
        p.subtitle { text-align: center; color: #666; margin-top: 0; }
        .row { display: flex; justify-content: space-between; margin: 12px 0; border-bottom: 1px dashed #eee; padding-bottom: 8px; }
        .total { font-size: 1.3rem; font-weight: bold; color: #8b0000; border-top: 2px solid #8b0000; padding-top: 15px; margin-top: 15px; }
    </style>
</head>
<body>
    <div class='receipt-card'>
        <h2>Abhinaya Institute</h2>
        <p class='subtitle'>Official Fee Payment Receipt</p>
        <div class='row'><span>Student Name:</span><strong>$full_name</strong></div>
        <div class='row'><span>Email:</span><strong>$email</strong></div>
        <div class='row'><span>Course:</span><strong>$course</strong></div>
        <div class='row'><span>Transaction ID:</span><strong>$txn_id</strong></div>
        <div class='row'><span>Date:</span><strong>$date</strong></div>
        <div class='row total'><span>Total Amount Paid:</span><span>₹$fee</span></div>
    </div>
</body>
</html>";

    $receipt_filename = $target_dir . "receipt_" . time() . "_" . $txn_id . ".html";
    file_put_contents($receipt_filename, $receipt_content);
    
    $sql = "INSERT INTO payments (full_name, email, course, payment_receipt) 
            VALUES ('$full_name', '$email', '$course', '$receipt_filename')";

    if (mysqli_query($conn, $sql)) {
        $_SESSION['receipt_data'] = [
            'name' => $full_name,
            'course' => $course,
            'amount' => $fee,
            'date' => $date,
            'transaction_id' => $txn_id,
            'file_path' => $receipt_filename
        ];
        header("Location: receipt.php");
        exit();
    } else {
        $message = "<p style='color: #ff6b6b; background: rgba(255,107,107,0.1); padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center;'>Error submitting payment: " . mysqli_error($conn) . "</p>";
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fee Payment - Abhinaya Institute of Classical Bharatanatyam</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body {
            font-family: 'Poppins', sans-serif;
            background:#0a0a0a;
            color: white;
            overflow-x: hidden;
        }
        /* Background Glow */
        body::before {
            content: '';
            position: fixed;
            width: 400px;
            height: 400px;
            background: #d4af37;
            border-radius: 50%;
            filter: blur(180px);
            top: -150px;
            left: -100px;
            opacity: 0.20;
            z-index: -1;
        }
        body::after {
            content: '';
            position: fixed;
            width: 350px;
            height: 350px;
            background: #8b0000;
            border-radius: 50%;
            filter: blur(180px);
            right: -100px;
            bottom: -100px;
            opacity: 0.15;
            z-index: -1;
        }
        /* Navbar */
        nav {
            position: fixed;
            top: 0;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 70px;
            background: rgba(0, 0, 0, 0.25);
            backdrop-filter: blur(15px);
            z-index: 999;
        }
        .logo { display: flex; align-items: center; font-family: 'Cinzel', serif; font-size: 1.5rem; font-weight: 700; color: #d4af37; text-decoration: none; }
        nav ul { display: flex; gap: 30px; list-style: none; align-items: center; }
        nav ul li a { color: white; text-decoration: none; transition: 0.3s; font-weight: 500; }
        nav ul li a:hover { color: #d4af37; }
        
        /* Dropdown Styles */
        .dropdown { position: relative; }
        .dropdown-content {
            display: none;
            position: absolute;
            background: rgba(10, 10, 10, 0.95);
            min-width: 200px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.5);
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 10px;
            overflow: hidden;
            top: 100%;
            left: 0;
            z-index: 1000;
        }
        .dropdown-content a {
            color: white;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            transition: 0.3s;
        }
        .dropdown-content a:hover {
            background-color: rgba(212, 175, 55, 0.1);
            color: #d4af37;
        }
        .dropdown:hover .dropdown-content { display: block; }
        
        /* Hero Section */
        .hero {
            height: 40vh;
            min-height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('images/slide1.jpg.jpg') center/cover;
            padding-top: 80px;
        }
        .hero-content h1 {
            font-family: 'Cinzel', serif;
            font-size: 3.5rem;
            color: #d4af37;
            margin-bottom: 10px;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
        }

        /* QR Code section styling */
        #qr-container {
            display: none;
            background: rgba(255,255,255,0.05);
            padding: 25px;
            border-radius: 15px;
            border: 1px solid rgba(212,175,55,0.3);
            margin: 25px 0;
            text-align: center;
            animation: fadeIn 0.5s ease-out;
        }
        #qr-container img {
            width: 210px;
            height: 210px;
            border-radius: 12px;
            margin: 15px auto;
            border: 6px solid white;
            background: white;
            display: block;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Form inputs styling */
        .form-group input, .form-group select {
            width: 100%;
            padding: 14px;
            background: rgba(0,0,0,0.6);
            border: 1px solid rgba(212,175,55,0.4);
            color: white;
            border-radius: 8px;
            font-family: 'Poppins', sans-serif;
            font-size: 1rem;
            outline: none;
            transition: 0.3s;
        }
        .form-group input:focus, .form-group select:focus {
            border-color: #d4af37;
            background: rgba(212,175,55,0.05);
        }
        
        /* Footer */
        .footer {
            background: #5b180f;
            padding: 50px 8% 20px;
        }
    </style>

<style>
/* Global Premium Transitions Override */
nav {
    transform: translateY(-100%);
    animation: slideDown 0.8s cubic-bezier(0.165, 0.84, 0.44, 1) forwards !important;
}
@keyframes slideDown {
    from { transform: translateY(-100%); }
    to { transform: translateY(0); }
}
nav ul li a {
    position: relative;
    padding-bottom: 5px;
    transition: color 0.3s !important;
}
nav ul li a::after {
    content: '';
    position: absolute;
    width: 100%;
    transform: scaleX(0);
    height: 2px;
    bottom: 0;
    left: 0;
    background-color: #d4af37;
    transform-origin: bottom right;
    transition: transform 0.3s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
}
nav ul li a:hover::after {
    transform: scaleX(1);
    transform-origin: bottom left;
}
.dropdown-content {
    display: block !important;
    opacity: 0;
    visibility: hidden;
    transform: translateY(15px);
    transition: opacity 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), visibility 0.4s !important;
    top: 105% !important;
}
.dropdown:hover .dropdown-content {
    opacity: 1 !important;
    visibility: visible !important;
    transform: translateY(0) !important;
}
footer.footer {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 1s cubic-bezier(0.165, 0.84, 0.44, 1), transform 1s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
}
footer.footer.active {
    opacity: 1 !important;
    transform: translateY(0) !important;
}
</style>
</head>
<body>
<nav>
    <a href="home.html" class="logo">
        <img src="https://abhinayaainstitute.org/wp-content/uploads/2025/10/AIRF-Favicon.png" alt="Abhinaya Logo" style="max-width:70px !important;">
    </a>
    <ul>
        <li><a href="home.html">Home</a></li>
        <li class="dropdown">
            <a href="#">About ▼</a>
            <div class="dropdown-content">
                <a href="guru.html">Our guru</a>
                <a href="about.html">The institute</a>
            </div>
        </li>
<li><a href="gallery.html">Gallery</a></li>
        <li class="dropdown">
            <a href="#">Students ▼</a>
            <div class="dropdown-content">
                <a href="The Bharatanatyam Learning Compendium.pdf" target="_blank">E-Book</a>            
                <a href="https://docs.google.com/forms/d/e/1FAIpQLSeoto6_5Cs139HBzN0_7P20A8oqpkJ3sCaSuMCh--0_UjTdkQ/viewform?usp=dialog">Online Admission 2026-27</a>
                <a href="core-team.html">Core Team</a>
                <a href="ACADEMIC CALENDAR.pdf" target="_blank">Academic Calendar</a>
                <a href="examinations.html">Examinations</a>
                <a href="events-workshops.html">Events & Workshops</a>
            </div>
        </li>
        <li><a href="student-portal.php">Students Portal</a></li>
        <li><a href="contact.html">Contact</a></li>
    </ul>
</nav>

<section class="hero">
    <div class="hero-content">
        <h1 class="page-title">Fee Payment</h1>
    </div>
</section>

<section class="form-section" style="padding: 70px 10%; max-width: 750px; margin: auto;">
    <h2 class="section-title" style="text-align:center; font-size:2.8rem; font-family:'Cinzel',serif; color:#d4af37; margin-bottom:15px;">Pay Annual Course Fee</h2>
    <p style="text-align: center; color: #ccc; margin-bottom: 30px;">Select your course, scan to pay instantly via UPI, and receive your verified fee receipt.</p>
    
    <?php echo $message; ?>
    
    <div class="form-container" style="background:rgba(255,255,255,.05); backdrop-filter:blur(15px); padding:40px; border-radius:25px; border:1px solid rgba(212,175,55,0.2); box-shadow: 0 15px 35px rgba(0,0,0,0.5);">
        <form action="" method="POST" id="fee-form">
            <div class="form-group" style="margin-bottom: 20px;">
                <label for="full_name" style="display: block; margin-bottom: 8px; color: #f8d76d; font-weight: 500;">Full Name *</label>
                <input type="text" id="full_name" name="full_name" required placeholder="Enter student full name">
            </div>
            
            <div class="form-group" style="margin-bottom: 20px;">
                <label for="email" style="display: block; margin-bottom: 8px; color: #f8d76d; font-weight: 500;">Email Address *</label>
                <input type="email" id="email" name="email" required placeholder="Enter student email address">
            </div>
            
            <div class="form-group" style="margin-bottom: 20px;">
                <label for="course-select" style="display: block; margin-bottom: 8px; color: #f8d76d; font-weight: 500;">Select Course and Annual fees *</label>
                <select id="course-select" name="course" required>
                    <option value="" style="color: black;">-- Select Course & Fee --</option>
                    <option value="Fresh Admission (Beginner) - ₹2000" data-fee="2000" style="color: black;">Fresh Admission (Beginner) – ₹2,000</option>
                    <option value="Prarambhik - ₹3000" data-fee="3000" style="color: black;">Prarambhik – ₹3,000</option>
                    <option value="Praveshika Pratham - ₹4000" data-fee="4000" style="color: black;">Praveshika Pratham – ₹4,000</option>
                    <option value="Praveshika Purna - ₹5000" data-fee="5000" style="color: black;">Praveshika Purna – ₹5,000</option>
                    <option value="Madhyama Pratham - ₹6000" data-fee="6000" style="color: black;">Madhyama Pratham – ₹6,000</option>
                    <option value="Madhyama Purna - ₹7000" data-fee="7000" style="color: black;">Madhyama Purna – ₹7,000</option>
                    <option value="Visharad Pratham - ₹8000" data-fee="8000" style="color: black;">Visharad Pratham – ₹8,000</option>
                    <option value="Visharad Dwitiya - ₹9000" data-fee="9000" style="color: black;">Visharad Dwitiya – ₹9,000</option>
                    <option value="Visharad Tritiya - ₹10000" data-fee="10000" style="color: black;">Visharad Tritiya – ₹10,000</option>
                    <option value="Alankar Pratham - ₹12000" data-fee="12000" style="color: black;">Alankar Pratham – ₹12,000</option>
                </select>
            </div>
            
            <div id="qr-container">
                <h3 style="color: #f8d76d; margin-bottom: 8px; font-family: 'Cinzel', serif;">Scan & Pay Fee</h3>
                <p style="font-size: 1rem; color: #ddd; margin-bottom: 5px;">Total Amount: <strong style="color: #f8d76d; font-size: 1.3rem;" id="display-fee"></strong></p>
                <img id="qr-code-img" src="" alt="UPI QR Code">
                <p style="font-size: 0.85rem; color: #bbb; margin-top: 10px;">Scan using <strong>Google Pay / PhonePe / Paytm</strong>. The exact course amount will be pre-filled automatically.</p>
            </div>
            
            <button type="submit" id="submit-btn" class="btn-submit" style="width: 100%; padding: 15px; background: linear-gradient(135deg, #d4af37, #f8d76d); color: black; font-weight: 600; border: none; border-radius: 50px; cursor: pointer; transition: 0.4s; font-family: 'Poppins', sans-serif; font-size: 1.1rem; margin-top: 15px;">Submit Payment</button>
        </form>
    </div>
</section>

<footer class="footer" style="background: #5b180f; padding: 50px 8% 20px;">
    <div class="footer-container" style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 40px;">
        <div class="footer-left" style="text-align: left;">
            <img src="https://abhinayaainstitute.org/wp-content/uploads/2025/10/AIRF-Favicon.png" alt="AIRF Logo" style="width: 50px; margin-bottom: 15px;">
            <h2 style="font-family: 'Cinzel', serif; font-size: 2rem; color: white; margin: 0;">Art. Discipline. Devotion.</h2>
        </div>
        <div class="footer-links" style="display: flex; gap: 80px; text-align: left;">
            <div style="display: flex; flex-direction: column; gap: 12px;">
                <a href="home.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">Home</a>
                <a href="about.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">About</a>
                <a href="guru.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">Our Guru</a>
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px;">
                <a href="gallery.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">Gallery</a>
                <a href="events-workshops.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">Events</a>
                <a href="contact.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">Contact</a>
                <a href="examinations.html" style="color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; font-size: 1rem;">Examinations</a>
            </div>
        </div>
    </div>
    <div class="footer-bottom" style="display: flex; justify-content: space-between; align-items: center; margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 20px;">
        <p style="color: white; margin: 0; font-size: 0.9rem;">&copy;2026 AIRF. All rights reserved.</p>
        <div class="social-icons" style="display: flex; gap: 15px;">
            <a href="https://www.instagram.com/abhinayaa_dance_institute" target="_blank" style="width: 35px; height: 35px; border-radius: 50%; background: white; color: #5b180f; display: flex; align-items: center; justify-content: center; text-decoration: none; font-size: 1.1rem;"><i class="fab fa-instagram"></i></a>
            <a href="https://www.facebook.com/abhinayaainstitute/" target="_blank" style="width: 35px; height: 35px; border-radius: 50%; background: white; color: #5b180f; display: flex; align-items: center; justify-content: center; text-decoration: none; font-size: 1.1rem;"><i class="fab fa-facebook-f"></i></a>
            <a href="https://www.youtube.com/@Abhinayaa_dance_institute" target="_blank" style="width: 35px; height: 35px; border-radius: 50%; background: white; color: #5b180f; display: flex; align-items: center; justify-content: center; text-decoration: none; font-size: 1.1rem;"><i class="fab fa-youtube"></i></a>
            <a href="#" style="width: 35px; height: 35px; border-radius: 50%; background: white; color: #5b180f; display: flex; align-items: center; justify-content: center; text-decoration: none; font-size: 1.1rem;"><i class="fas fa-chevron-up"></i></a>
        </div>
    </div>
</footer>

<script>
document.addEventListener("DOMContentLoaded", function() {
    const courseSelect = document.getElementById('course-select');
    const qrContainer = document.getElementById('qr-container');
    const qrCodeImg = document.getElementById('qr-code-img');
    const displayFee = document.getElementById('display-fee');
    const submitBtn = document.getElementById('submit-btn');
    
    // Business UPI credentials
    const businessUPI = 'sanchisonabolke19@okaxis'; 
    const businessName = 'Sanchisona Bolke';

    courseSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        const fee = selectedOption.getAttribute('data-fee');
        
        if (fee) {
            // Construct UPI URI with embedded amount
            const upiURI = `upi://pay?pa=${businessUPI}&pn=${encodeURIComponent(businessName)}&am=${fee}&cu=INR`;
            
            // Generate dynamic QR Code
            const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=210x210&data=${encodeURIComponent(upiURI)}`;
            
            qrCodeImg.src = qrUrl;
            displayFee.textContent = '₹' + Number(fee).toLocaleString('en-IN');
            qrContainer.style.display = 'block';
            submitBtn.textContent = 'Confirm Payment & Generate Receipt';
        } else {
            qrContainer.style.display = 'none';
            submitBtn.textContent = 'Submit Payment';
        }
    });
});
</script>

<script>
document.addEventListener("DOMContentLoaded", function() {
    var reveals = document.querySelectorAll(".reveal, .reveal-left, .reveal-right, footer");
    var observer = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("active");
                observer.unobserve(entry.target);
            }
        });
    }, { rootMargin: "0px 0px -30px 0px" });
    
    reveals.forEach(function(reveal) {
        observer.observe(reveal);
    });
});
</script>

<!-- AI Chat Widget -->
<!-- AI Chat Widget -->
<div id="ai-chat-widget-container">
    <!-- Floating Chat Trigger Button -->
    <button id="ai-chat-toggle" aria-label="Open AI Assistant" title="Need help? Ask Abhinaya AI">
        <i class="fa fa-comments" id="chat-icon-open"></i>
        <i class="fa fa-times" id="chat-icon-close" style="display: none;"></i>
        <span class="chat-badge">AI</span>
    </button>

    <!-- Chat Window Modal -->
    <div id="ai-chat-window">
        <div class="chat-header">
            <div class="chat-header-info">
                <div class="chat-avatar">
                    <img src="https://abhinayaainstitute.org/wp-content/uploads/2025/10/AIRF-Favicon.png" alt="AI Avatar">
                    <span class="status-dot"></span>
                </div>
                <div>
                    <h4>Abhinaya AI Assistant</h4>
                    <p class="status-text">Online • Classical Support</p>
                </div>
            </div>
            <button id="ai-chat-close" title="Close Chat">&times;</button>
        </div>

        <div class="chat-messages" id="chat-messages">
            <div class="message bot-msg">
                <div class="msg-content">
                    Namaste! 🙏 I am your <strong>Abhinaya Virtual Assistant</strong>. How can I help you navigate our classical dance portal today?
                </div>
            </div>
            
            <div class="quick-chips" id="quick-chips">
                <button onclick="sendQuickMessage('What courses and syllabus are offered?')">🎭 Courses</button>
                <button onclick="sendQuickMessage('How to pay annual course fees?')">💳 Fee Payment</button>
                <button onclick="sendQuickMessage('How to register a new account?')">📝 Registration</button>
                <button onclick="sendQuickMessage('How to login or reset password?')">🔑 Login / Password</button>
                <button onclick="sendQuickMessage('Examination and attendance rules')">📅 Exams & Schedule</button>
            </div>
        </div>

        <div class="chat-typing-indicator" id="chat-typing" style="display: none;">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>

        <div class="chat-input-area">
            <input type="text" id="chat-input" placeholder="Ask about courses, fees, portal..." autocomplete="off">
            <button id="chat-send-btn" title="Send Message">
                <i class="fa fa-paper-plane"></i>
            </button>
        </div>
    </div>
</div>

<style>
/* AI Chatbot Styles */
#ai-chat-widget-container {
    position: fixed;
    bottom: 25px;
    right: 25px;
    z-index: 99999;
    font-family: 'Poppins', sans-serif;
}

#ai-chat-toggle {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #d4af37, #8b0000);
    border: 2px solid rgba(255, 255, 255, 0.4);
    box-shadow: 0 8px 25px rgba(212, 175, 55, 0.4);
    color: white;
    font-size: 1.5rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s;
}

#ai-chat-toggle:hover {
    transform: scale(1.08);
    box-shadow: 0 12px 30px rgba(212, 175, 55, 0.6);
}

.chat-badge {
    position: absolute;
    top: -4px;
    right: -4px;
    background: #4cd137;
    color: black;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 10px;
    border: 1px solid white;
    letter-spacing: 0.5px;
}

#ai-chat-window {
    display: none;
    position: absolute;
    bottom: 75px;
    right: 0;
    width: 380px;
    height: 520px;
    max-height: 80vh;
    background: rgba(15, 15, 15, 0.95);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(212, 175, 55, 0.35);
    border-radius: 20px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8);
    flex-direction: column;
    overflow: hidden;
    animation: chatPopUp 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes chatPopUp {
    from { opacity: 0; transform: translateY(20px) scale(0.95); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

.chat-header {
    background: linear-gradient(135deg, rgba(139, 0, 0, 0.9), rgba(20, 20, 20, 0.9));
    padding: 16px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(212, 175, 55, 0.3);
}

.chat-header-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.chat-avatar {
    position: relative;
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #d4af37;
}

.chat-avatar img {
    width: 26px;
    height: 26px;
}

.status-dot {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 10px;
    height: 10px;
    background: #4cd137;
    border-radius: 50%;
    border: 2px solid #0f0f0f;
}

.chat-header h4 {
    margin: 0;
    font-family: 'Cinzel', serif;
    color: #f8d76d;
    font-size: 1.05rem;
}

.status-text {
    margin: 0;
    font-size: 0.75rem;
    color: #bbb;
}

#ai-chat-close {
    background: transparent;
    border: none;
    color: white;
    font-size: 1.5rem;
    cursor: pointer;
    transition: color 0.2s;
    line-height: 1;
}

#ai-chat-close:hover {
    color: #ff6b6b;
}

.chat-messages {
    flex: 1;
    padding: 16px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.chat-messages::-webkit-scrollbar {
    width: 5px;
}
.chat-messages::-webkit-scrollbar-thumb {
    background: rgba(212, 175, 55, 0.3);
    border-radius: 10px;
}

.message {
    display: flex;
    max-width: 88%;
}

.bot-msg {
    align-self: flex-start;
}

.user-msg {
    align-self: flex-end;
}

.msg-content {
    padding: 12px 16px;
    border-radius: 14px;
    font-size: 0.9rem;
    line-height: 1.5;
}

.bot-msg .msg-content {
    background: rgba(255, 255, 255, 0.08);
    color: #f0f0f0;
    border: 1px solid rgba(212, 175, 55, 0.2);
    border-top-left-radius: 2px;
}

.user-msg .msg-content {
    background: linear-gradient(135deg, #d4af37, #f8d76d);
    color: black;
    font-weight: 500;
    border-top-right-radius: 2px;
}

.quick-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 5px;
}

.quick-chips button {
    background: rgba(212, 175, 55, 0.12);
    border: 1px solid rgba(212, 175, 55, 0.35);
    color: #f8d76d;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 0.75rem;
    cursor: pointer;
    transition: 0.2s;
    font-family: 'Poppins', sans-serif;
}

.quick-chips button:hover {
    background: #d4af37;
    color: black;
}

.chat-typing-indicator {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 8px 16px;
    background: rgba(255, 255, 255, 0.05);
    width: fit-content;
    border-radius: 12px;
    margin: 0 16px 8px;
}

.typing-dot {
    width: 6px;
    height: 6px;
    background: #d4af37;
    border-radius: 50%;
    animation: typingBounce 1.4s infinite ease-in-out both;
}

.typing-dot:nth-child(1) { animation-delay: -0.32s; }
.typing-dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes typingBounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
}

.chat-input-area {
    padding: 12px 16px;
    background: rgba(10, 10, 10, 0.95);
    border-top: 1px solid rgba(212, 175, 55, 0.2);
    display: flex;
    gap: 10px;
    align-items: center;
}

.chat-input-area input {
    flex: 1;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(212, 175, 55, 0.3);
    color: white;
    padding: 10px 14px;
    border-radius: 25px;
    font-family: 'Poppins', sans-serif;
    font-size: 0.9rem;
    outline: none;
    transition: border-color 0.3s;
}

.chat-input-area input:focus {
    border-color: #d4af37;
}

.chat-input-area button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #d4af37, #f8d76d);
    border: none;
    color: black;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s;
    font-size: 0.95rem;
}

.chat-input-area button:hover {
    transform: scale(1.05);
}

@media (max-width: 480px) {
    #ai-chat-window {
        width: calc(100vw - 30px);
        right: -10px;
        bottom: 70px;
        height: 480px;
    }
}
</style>

<script>
(function() {
    const toggleBtn = document.getElementById('ai-chat-toggle');
    const closeBtn = document.getElementById('ai-chat-close');
    const chatWindow = document.getElementById('ai-chat-window');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('chat-send-btn');
    const typingIndicator = document.getElementById('chat-typing');
    const iconOpen = document.getElementById('chat-icon-open');
    const iconClose = document.getElementById('chat-icon-close');

    if (!toggleBtn || !chatWindow) return;

    function toggleChat() {
        const isOpen = chatWindow.style.display === 'flex';
        if (isOpen) {
            chatWindow.style.display = 'none';
            iconOpen.style.display = 'block';
            iconClose.style.display = 'none';
        } else {
            chatWindow.style.display = 'flex';
            iconOpen.style.display = 'none';
            iconClose.style.display = 'block';
            chatInput.focus();
        }
    }

    toggleBtn.addEventListener('click', toggleChat);
    closeBtn.addEventListener('click', toggleChat);

    function appendMessage(sender, htmlContent) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-msg`;
        msgDiv.innerHTML = `<div class="msg-content">${htmlContent}</div>`;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    window.sendQuickMessage = function(text) {
        chatInput.value = text;
        sendMessage();
    };

    function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        appendMessage('user', text);
        chatInput.value = '';
        typingIndicator.style.display = 'flex';
        chatMessages.scrollTop = chatMessages.scrollHeight;

        fetch('chatbot_api.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: text })
        })
        .then(res => res.json())
        .then(data => {
            typingIndicator.style.display = 'none';
            if (data && data.response) {
                appendMessage('bot', data.response);
            } else {
                appendMessage('bot', 'I apologize, I encountered a brief glitch. Please try again!');
            }
        })
        .catch(err => {
            typingIndicator.style.display = 'none';
            appendMessage('bot', 'You can navigate to our <a href="courses.php" style="color:#d4af37; text-decoration:underline;">Courses Page</a> or <a href="contact.php" style="color:#d4af37; text-decoration:underline;">Contact Page</a> for direct assistance.');
        });
    }

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
})();
</script>
<!-- End AI Chat Widget -->
</body>
</html>
