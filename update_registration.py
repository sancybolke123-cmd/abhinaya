import re

with open('c:/Xamp/htdocs/abhinaya/home.html', 'r', encoding='utf-8') as f:
    home = f.read()

nav_match = re.search(r'<nav>.*?</nav>', home, re.DOTALL)
footer_match = re.search(r'<footer[^>]*>.*?</footer>', home, re.DOTALL)

nav_html = nav_match.group(0) if nav_match else ''
nav_html = nav_html.replace('student-portal.html', 'student-portal.php')
footer_html = footer_match.group(0) if footer_match else ''

portal_css = """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body { font-family: 'Poppins', sans-serif; background: #0a0a0a; color: white; overflow-x: hidden; }
        nav { position: fixed; top: 0; width: 100%; display: flex; justify-content: space-between; align-items: center; padding: 20px 70px; background: rgba(0, 0, 0, 0.25); backdrop-filter: blur(15px); z-index: 999; }
        .logo { display: flex; align-items: center; font-family: 'Cinzel', serif; font-size: 1.5rem; font-weight: 700; color: #d4af37; text-decoration: none; }
        nav ul { display: flex; gap: 30px; list-style: none; align-items: center; }
        nav ul li a { color: white; text-decoration: none; transition: 0.3s; font-weight: 500; }
        nav ul li a:hover { color: #d4af37; }
        .dropdown { position: relative; }
        .dropdown-content { display: none; position: absolute; background: rgba(10, 10, 10, 0.95); min-width: 200px; box-shadow: 0 8px 16px rgba(0,0,0,0.5); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 10px; overflow: hidden; top: 100%; left: 0; z-index: 1000; }
        .dropdown-content a { color: white; padding: 12px 16px; text-decoration: none; display: block; border-bottom: 1px solid rgba(255,255,255,0.05); transition: 0.3s; }
        .dropdown-content a:hover { background-color: rgba(212, 175, 55, 0.1); color: #d4af37; }
        .dropdown:hover .dropdown-content { display: block; }
        
        .portal-wrapper {
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
            padding: 120px 20px 60px;
        }
        .portal-box {
            background: rgba(10, 10, 10, 0.85); backdrop-filter: blur(20px);
            padding: 50px; border-radius: 20px; text-align: center; width: 100%; max-width: 500px;
            border: 1px solid rgba(212, 175, 55, 0.3); box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            animation: fadeIn 0.8s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .portal-box h2 { font-family: 'Cinzel', serif; font-size: 2.5rem; color: #d4af37; margin-bottom: 10px; }
        .portal-box p { color: #ccc; margin-bottom: 30px; font-size: 1.1rem; }
        
        .form-group { margin-bottom: 20px; text-align: left; }
        .form-group label { display: block; margin-bottom: 8px; color: #f8d76d; font-weight: 500; }
        .form-group input, .form-group select { width: 100%; padding: 15px; border-radius: 8px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2); color: white; font-family: 'Poppins', sans-serif; font-size: 1rem; outline: none; transition: 0.3s; }
        .form-group input:focus, .form-group select:focus { border-color: #d4af37; background: rgba(212,175,55,0.05); }
        
        .btn-submit { width: 100%; background: linear-gradient(135deg, #d4af37, #f8d76d); color: #0a0a0a; border: none; padding: 15px; font-size: 1.1rem; font-weight: 600; border-radius: 50px; cursor: pointer; transition: transform 0.3s, box-shadow 0.3s; margin-top: 10px; }
        .btn-submit:hover { transform: scale(1.02); box-shadow: 0 8px 20px rgba(212,175,55,0.4); }
        
        .error-msg { color: #ff6b6b; background: rgba(255,107,107,0.1); padding: 10px; border-radius: 5px; margin-bottom: 20px; border-left: 3px solid #ff6b6b; text-align: left; font-size: 0.9rem; }
        .success-msg { color: #4cd137; background: rgba(76,209,55,0.1); padding: 10px; border-radius: 5px; margin-bottom: 20px; border-left: 3px solid #4cd137; text-align: left; font-size: 0.9rem; }
        
        .portal-links { margin-top: 25px; font-size: 0.95rem; color: #aaa; }
        .portal-links a { color: #d4af37; text-decoration: none; font-weight: 500; transition: 0.3s; }
        .portal-links a:hover { color: #f8d76d; text-decoration: underline; }
"""

register_php = f"""<?php
session_start();
require 'config.php';

if (isset($_SESSION['user_id'])) {{
    header("Location: dashboard.php");
    exit();
}}

$error = '';
$success = '';

if ($_SERVER["REQUEST_METHOD"] == "POST") {{
    $fullname = trim($_POST['full_name']);
    $email = trim($_POST['email']);
    $password = $_POST['password'];
    $confirm_password = $_POST['confirm_password'];
    $course = $_POST['course'];
    
    if (empty($fullname) || empty($email) || empty($password) || empty($course)) {{
        $error = "Please fill in all required fields.";
    }} elseif ($password !== $confirm_password) {{
        $error = "Passwords do not match.";
    }} elseif (strlen($password) < 6) {{
        $error = "Password must be at least 6 characters long.";
    }} else {{
        $stmt = $pdo->prepare("SELECT id FROM users WHERE email = ?");
        $stmt->execute([$email]);
        if ($stmt->rowCount() > 0) {{
            $error = "Email address is already registered.";
        }} else {{
            $hashed_password = password_hash($password, PASSWORD_DEFAULT);
            $stmt = $pdo->prepare("INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)");
            if ($stmt->execute([$fullname, $email, $hashed_password])) {{
                
                // Extract amount from course string (e.g. "Beginner - ₹1500" -> 1500)
                preg_match('/₹(\\d+)/', $course, $matches);
                $amount = isset($matches[1]) ? $matches[1] : 0;
                
                // Save receipt data to session
                $_SESSION['receipt_data'] = [
                    'name' => $fullname,
                    'course' => $course,
                    'amount' => $amount,
                    'date' => date('Y-m-d H:i:s'),
                    'transaction_id' => 'TXN' . strtoupper(uniqid())
                ];
                
                header("Location: receipt.php");
                exit();
            }} else {{
                $error = "An error occurred during registration. Please try again.";
            }}
        }}
    }}
}}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register - Abhinaya Institute</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
{portal_css}
        .portal-wrapper {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)), url('images/slide2.jpg.jpg') center/cover fixed; }}
        
        /* QR Code section styling */
        #qr-container {{
            display: none;
            background: rgba(255,255,255,0.05);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid rgba(212,175,55,0.3);
            margin: 20px 0;
            animation: fadeIn 0.5s ease-out;
        }}
        #qr-container img {{
            width: 200px;
            height: 200px;
            border-radius: 10px;
            margin: 10px auto;
            border: 5px solid white;
            background: white;
        }}
    </style>
</head>
<body>
{nav_html}
<div class="portal-wrapper">
    <div class="portal-box" style="max-width: 600px;">
        <h2>Join Abhinaya</h2>
        <p>Create your student account & Pay Fee</p>
        
        <?php if($error): ?>
            <div class="error-msg"><i class="fa fa-exclamation-circle"></i> <?php echo htmlspecialchars($error); ?></div>
        <?php endif; ?>
        
        <form method="POST" action="register.php" id="register-form">
            <div style="display: flex; gap: 15px;">
                <div class="form-group" style="flex:1;">
                    <label>Full Name</label>
                    <input type="text" name="full_name" required placeholder="Enter your full name" value="<?php echo htmlspecialchars($_POST['full_name'] ?? ''); ?>">
                </div>
                <div class="form-group" style="flex:1;">
                    <label>Email Address</label>
                    <input type="email" name="email" required placeholder="Enter your email" value="<?php echo htmlspecialchars($_POST['email'] ?? ''); ?>">
                </div>
            </div>
            
            <div style="display: flex; gap: 15px;">
                <div class="form-group" style="flex:1;">
                    <label>Password</label>
                    <input type="password" name="password" required placeholder="Create a password">
                </div>
                <div class="form-group" style="flex:1;">
                    <label>Confirm Password</label>
                    <input type="password" name="confirm_password" required placeholder="Confirm your password">
                </div>
            </div>
            
            <div class="form-group">
                <label>Course Selection</label>
                <select name="course" id="course-select" required>
                    <option value="" style="color: black;">Select Course</option>
                    <option value="Beginner - ₹1500" data-fee="1500" style="color: black;">Beginner - ₹1500</option>
                    <option value="Prarambhik - ₹2000" data-fee="2000" style="color: black;">Prarambhik - ₹2000</option>
                    <option value="Praveshika Pratham - ₹2500" data-fee="2500" style="color: black;">Praveshika Pratham - ₹2500</option>
                    <option value="Praveshika Purna - ₹3000" data-fee="3000" style="color: black;">Praveshika Purna - ₹3000</option>
                    <option value="Madhyama Pratham - ₹3500" data-fee="3500" style="color: black;">Madhyama Pratham - ₹3500</option>
                    <option value="Madhyama Purna - ₹4000" data-fee="4000" style="color: black;">Madhyama Purna - ₹4000</option>
                    <option value="Visharad Pratham - ₹4500" data-fee="4500" style="color: black;">Visharad Pratham (Upantya Visharad) - ₹4500</option>
                    <option value="Visharad Purna - ₹5000" data-fee="5000" style="color: black;">Visharad Purna - ₹5000</option>
                    <option value="Alankar Pratham - ₹5500" data-fee="5500" style="color: black;">Alankar Pratham (Part I) - ₹5500</option>
                    <option value="Alankar Purna - ₹6000" data-fee="6000" style="color: black;">Alankar Purna (Part II) - ₹6000</option>
                </select>
            </div>
            
            <div id="qr-container">
                <h4 style="color: #f8d76d; margin-bottom: 10px;">Scan to Pay Fee</h4>
                <p style="font-size: 0.9rem; color: #ddd; margin-bottom: 10px;">Amount: <strong style="color: white; font-size: 1.1rem;" id="display-fee"></strong></p>
                <img id="qr-code-img" src="" alt="UPI QR Code">
                <p style="font-size: 0.8rem; color: #aaa; margin-top: 10px;">After successful payment via GPay/PhonePe/Paytm, click the button below to complete registration.</p>
            </div>

            <button type="submit" class="btn-submit" id="submit-btn">Register</button>
        </form>
        
        <div class="portal-links">
            Already have an account? <a href="login.php">Login here</a>
        </div>
    </div>
</div>
{footer_html}

<script>
document.addEventListener("DOMContentLoaded", function() {{
    const courseSelect = document.getElementById('course-select');
    const qrContainer = document.getElementById('qr-container');
    const qrCodeImg = document.getElementById('qr-code-img');
    const displayFee = document.getElementById('display-fee');
    const submitBtn = document.getElementById('submit-btn');
    
    // Replace this with your actual Business UPI ID
    const businessUPI = 'abhinaya@ybl'; 
    const businessName = 'Abhinaya Institute';

    courseSelect.addEventListener('change', function() {{
        const selectedOption = this.options[this.selectedIndex];
        const fee = selectedOption.getAttribute('data-fee');
        
        if (fee) {{
            // Construct UPI URI
            const upiURI = `upi://pay?pa=${{businessUPI}}&pn=${{encodeURIComponent(businessName)}}&am=${{fee}}&cu=INR`;
            
            // Generate QR Code using free API
            const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${{encodeURIComponent(upiURI)}}`;
            
            qrCodeImg.src = qrUrl;
            displayFee.textContent = '₹' + fee;
            qrContainer.style.display = 'block';
            submitBtn.textContent = 'Confirm Payment & Register';
        }} else {{
            qrContainer.style.display = 'none';
            submitBtn.textContent = 'Register';
        }}
    }});
}});
</script>

</body>
</html>
"""

receipt_php = f"""<?php
session_start();

if (!isset($_SESSION['receipt_data'])) {{
    header("Location: student-portal.php");
    exit();
}}

$receipt = $_SESSION['receipt_data'];
// Clear the receipt data so it isn't shown again if they refresh later
// unset($_SESSION['receipt_data']); 
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fee Receipt - Abhinaya Institute</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
{portal_css}
        .portal-wrapper {{ background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), url('images/Bharatanatyam Dance - Indian Dance.jpg') center/cover fixed; }}
        
        .receipt-card {{
            background: white;
            color: #161514;
            padding: 40px;
            border-radius: 10px;
            max-width: 500px;
            margin: 0 auto;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            position: relative;
            text-align: left;
        }}
        .receipt-card::before {{
            content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 10px;
            background: linear-gradient(90deg, #d4af37, #8b0000);
            border-radius: 10px 10px 0 0;
        }}
        .receipt-header {{
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px dashed #ddd;
            padding-bottom: 20px;
        }}
        .receipt-header h2 {{ font-family: 'Cinzel', serif; color: #8b0000; font-size: 2rem; margin-bottom: 5px; }}
        .receipt-header p {{ color: #666; font-size: 0.9rem; }}
        
        .receipt-row {{ display: flex; justify-content: space-between; margin-bottom: 15px; font-size: 1.1rem; }}
        .receipt-row .label {{ color: #666; font-weight: 500; }}
        .receipt-row .value {{ font-weight: 600; color: #333; text-align: right; max-width: 60%; }}
        
        .receipt-total {{
            margin-top: 20px; padding-top: 20px; border-top: 2px solid #eee;
            display: flex; justify-content: space-between; font-size: 1.5rem; font-weight: 700; color: #8b0000;
        }}
        
        .btn-print {{
            display: block; width: 100%; text-align: center; background: #8b0000; color: white;
            padding: 15px; border-radius: 8px; text-decoration: none; font-weight: 600;
            margin-top: 30px; transition: 0.3s; cursor: pointer; border: none; font-family: 'Poppins', sans-serif;
        }}
        .btn-print:hover {{ background: #5b180f; }}
        
        .login-btn {{
            display: block; width: 100%; text-align: center; background: transparent; color: #8b0000; border: 2px solid #8b0000;
            padding: 15px; border-radius: 8px; text-decoration: none; font-weight: 600;
            margin-top: 15px; transition: 0.3s;
        }}
        .login-btn:hover {{ background: rgba(139,0,0,0.05); }}
        
        /* Print styles */
        @media print {{
            body * {{ visibility: hidden; }}
            .receipt-card, .receipt-card * {{ visibility: visible; }}
            .receipt-card {{ position: absolute; left: 0; top: 0; width: 100%; max-width: 100%; box-shadow: none; border: 1px solid #ccc; }}
            .btn-print, .login-btn, nav, footer {{ display: none !important; }}
        }}
    </style>
</head>
<body>
{nav_html}
<div class="portal-wrapper">
    <div style="width: 100%; max-width: 600px; text-align: center;">
        <h2 style="color: #4cd137; margin-bottom: 20px;"><i class="fa fa-check-circle"></i> Payment Successful!</h2>
        <div class="receipt-card">
            <div class="receipt-header">
                <h2>Abhinaya Institute</h2>
                <p>Fee Payment Receipt</p>
            </div>
            
            <div class="receipt-row">
                <span class="label">Date:</span>
                <span class="value"><?php echo htmlspecialchars($receipt['date']); ?></span>
            </div>
            <div class="receipt-row">
                <span class="label">Transaction ID:</span>
                <span class="value"><?php echo htmlspecialchars($receipt['transaction_id']); ?></span>
            </div>
            <div class="receipt-row">
                <span class="label">Student Name:</span>
                <span class="value"><?php echo htmlspecialchars($receipt['name']); ?></span>
            </div>
            <div class="receipt-row">
                <span class="label">Course:</span>
                <span class="value"><?php echo htmlspecialchars($receipt['course']); ?></span>
            </div>
            
            <div class="receipt-total">
                <span>Total Paid:</span>
                <span>₹<?php echo htmlspecialchars($receipt['amount']); ?></span>
            </div>
            
            <button onclick="window.print()" class="btn-print"><i class="fa fa-print"></i> Print / Save as PDF</button>
            <a href="login.php" class="login-btn">Proceed to Login</a>
        </div>
    </div>
</div>
{footer_html}
</body>
</html>
"""

with open('c:/Xamp/htdocs/abhinaya/register.php', 'w', encoding='utf-8') as f:
    f.write(register_php)

with open('c:/Xamp/htdocs/abhinaya/receipt.php', 'w', encoding='utf-8') as f:
    f.write(receipt_php)

print("Updated register.php and created receipt.php.")
