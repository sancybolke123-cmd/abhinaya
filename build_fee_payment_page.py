import re

with open('c:/Xamp/htdocs/abhinaya/home.html', 'r', encoding='utf-8') as f:
    home = f.read()

nav_match = re.search(r'<nav>.*?</nav>', home, re.DOTALL)
footer_match = re.search(r'<footer[^>]*>.*?</footer>', home, re.DOTALL)

nav_html = nav_match.group(0) if nav_match else ''
nav_html = nav_html.replace('student-portal.html', 'student-portal.php')
footer_html = footer_match.group(0) if footer_match else ''

content = f"""<?php
session_start();
require 'db.php';

$message = "";
if ($_SERVER["REQUEST_METHOD"] == "POST") {{
    $full_name = mysqli_real_escape_string($conn, trim($_POST['full_name']));
    $email = mysqli_real_escape_string($conn, trim($_POST['email']));
    $course = mysqli_real_escape_string($conn, trim($_POST['course']));
    
    // Extract fee from course value
    preg_match('/₹(\\d+)/', $course, $matches);
    $fee = isset($matches[1]) ? $matches[1] : '0';
    
    $txn_id = 'TXN' . strtoupper(uniqid());
    $date = date('Y-m-d H:i:s');
    
    $target_dir = "uploads/";
    if (!is_dir($target_dir)) {{
        mkdir($target_dir, 0777, true);
    }}
    
    $receipt_content = "<!DOCTYPE html>
<html>
<head>
    <title>Fee Receipt - $txn_id</title>
    <style>
        body {{ font-family: 'Poppins', sans-serif; background: #fafafa; padding: 40px; }}
        .receipt-card {{ background: white; max-width: 500px; margin: auto; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 6px solid #8b0000; }}
        h2 {{ color: #8b0000; text-align: center; margin-bottom: 5px; font-family: 'Cinzel', serif; }}
        p.subtitle {{ text-align: center; color: #666; margin-top: 0; }}
        .row {{ display: flex; justify-content: space-between; margin: 12px 0; border-bottom: 1px dashed #eee; padding-bottom: 8px; }}
        .total {{ font-size: 1.3rem; font-weight: bold; color: #8b0000; border-top: 2px solid #8b0000; padding-top: 15px; margin-top: 15px; }}
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

    if (mysqli_query($conn, $sql)) {{
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
    }} else {{
        $message = "<p style='color: #ff6b6b; background: rgba(255,107,107,0.1); padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center;'>Error submitting payment: " . mysqli_error($conn) . "</p>";
    }}
}}
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
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; }}
        body {{
            font-family: 'Poppins', sans-serif;
            background:#0a0a0a;
            color: white;
            overflow-x: hidden;
        }}
        /* Background Glow */
        body::before {{
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
        }}
        body::after {{
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
        }}
        /* Navbar */
        nav {{
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
        }}
        .logo {{ display: flex; align-items: center; font-family: 'Cinzel', serif; font-size: 1.5rem; font-weight: 700; color: #d4af37; text-decoration: none; }}
        nav ul {{ display: flex; gap: 30px; list-style: none; align-items: center; }}
        nav ul li a {{ color: white; text-decoration: none; transition: 0.3s; font-weight: 500; }}
        nav ul li a:hover {{ color: #d4af37; }}
        
        /* Dropdown Styles */
        .dropdown {{ position: relative; }}
        .dropdown-content {{
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
        }}
        .dropdown-content a {{
            color: white;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            transition: 0.3s;
        }}
        .dropdown-content a:hover {{
            background-color: rgba(212, 175, 55, 0.1);
            color: #d4af37;
        }}
        .dropdown:hover .dropdown-content {{ display: block; }}
        
        /* Hero Section */
        .hero {{
            height: 40vh;
            min-height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('images/slide1.jpg.jpg') center/cover;
            padding-top: 80px;
        }}
        .hero-content h1 {{
            font-family: 'Cinzel', serif;
            font-size: 3.5rem;
            color: #d4af37;
            margin-bottom: 10px;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
        }}

        /* QR Code section styling */
        #qr-container {{
            display: none;
            background: rgba(255,255,255,0.05);
            padding: 25px;
            border-radius: 15px;
            border: 1px solid rgba(212,175,55,0.3);
            margin: 25px 0;
            text-align: center;
            animation: fadeIn 0.5s ease-out;
        }}
        #qr-container img {{
            width: 210px;
            height: 210px;
            border-radius: 12px;
            margin: 15px auto;
            border: 6px solid white;
            background: white;
            display: block;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Form inputs styling */
        .form-group input, .form-group select {{
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
        }}
        .form-group input:focus, .form-group select:focus {{
            border-color: #d4af37;
            background: rgba(212,175,55,0.05);
        }}
        
        /* Footer */
        .footer {{
            background: #5b180f;
            padding: 50px 8% 20px;
        }}
    </style>

<style>
/* Global Premium Transitions Override */
nav {{
    transform: translateY(-100%);
    animation: slideDown 0.8s cubic-bezier(0.165, 0.84, 0.44, 1) forwards !important;
}}
@keyframes slideDown {{
    from {{ transform: translateY(-100%); }}
    to {{ transform: translateY(0); }}
}}
nav ul li a {{
    position: relative;
    padding-bottom: 5px;
    transition: color 0.3s !important;
}}
nav ul li a::after {{
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
}}
nav ul li a:hover::after {{
    transform: scaleX(1);
    transform-origin: bottom left;
}}
.dropdown-content {{
    display: block !important;
    opacity: 0;
    visibility: hidden;
    transform: translateY(15px);
    transition: opacity 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), visibility 0.4s !important;
    top: 105% !important;
}}
.dropdown:hover .dropdown-content {{
    opacity: 1 !important;
    visibility: visible !important;
    transform: translateY(0) !important;
}}
footer.footer {{
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 1s cubic-bezier(0.165, 0.84, 0.44, 1), transform 1s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
}}
footer.footer.active {{
    opacity: 1 !important;
    transform: translateY(0) !important;
}}
</style>
</head>
<body>
{nav_html}

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
        <form action="fee-payment.php" method="POST" id="fee-form">
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

{footer_html}

<script>
document.addEventListener("DOMContentLoaded", function() {{
    const courseSelect = document.getElementById('course-select');
    const qrContainer = document.getElementById('qr-container');
    const qrCodeImg = document.getElementById('qr-code-img');
    const displayFee = document.getElementById('display-fee');
    const submitBtn = document.getElementById('submit-btn');
    
    // Business UPI credentials
    const businessUPI = 'sanchisonabolke19@okaxis'; 
    const businessName = 'Sanchisona Bolke';

    courseSelect.addEventListener('change', function() {{
        const selectedOption = this.options[this.selectedIndex];
        const fee = selectedOption.getAttribute('data-fee');
        
        if (fee) {{
            // Construct UPI URI with embedded amount
            const upiURI = `upi://pay?pa=${{businessUPI}}&pn=${{encodeURIComponent(businessName)}}&am=${{fee}}&cu=INR`;
            
            // Generate dynamic QR Code
            const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=210x210&data=${{encodeURIComponent(upiURI)}}`;
            
            qrCodeImg.src = qrUrl;
            displayFee.textContent = '₹' + Number(fee).toLocaleString('en-IN');
            qrContainer.style.display = 'block';
            submitBtn.textContent = 'Confirm Payment & Generate Receipt';
        }} else {{
            qrContainer.style.display = 'none';
            submitBtn.textContent = 'Submit Payment';
        }}
    }});
}});
</script>

<script>
document.addEventListener("DOMContentLoaded", function() {{
    var reveals = document.querySelectorAll(".reveal, .reveal-left, .reveal-right, footer");
    var observer = new IntersectionObserver(function(entries, observer) {{
        entries.forEach(function(entry) {{
            if (entry.isIntersecting) {{
                entry.target.classList.add("active");
                observer.unobserve(entry.target);
            }}
        }});
    }}, {{ rootMargin: "0px 0px -30px 0px" }});
    
    reveals.forEach(function(reveal) {{
        observer.observe(reveal);
    }});
}});
</script>
</body>
</html>
"""

with open('c:/Xamp/htdocs/abhinaya/fee-payment.php', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated fee-payment.php successfully!")
