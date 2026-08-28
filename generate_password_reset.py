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

forgot_php = f"""<?php
session_start();
require 'config.php';

if (isset($_SESSION['user_id'])) {{
    header("Location: dashboard.php");
    exit();
}}

$error = '';
$success = '';
$code_generated = false;

if ($_SERVER["REQUEST_METHOD"] == "POST") {{
    $email = trim($_POST['email']);
    
    if (empty($email)) {{
        $error = "Please enter your email address.";
    }} else {{
        $stmt = $pdo->prepare("SELECT id, full_name FROM users WHERE email = ?");
        $stmt->execute([$email]);
        $user = $stmt->fetch();
        
        if ($user) {{
            $code = rand(100000, 999999);
            $_SESSION['reset_code'] = $code;
            $_SESSION['reset_email'] = $email;
            $_SESSION['reset_time'] = time();
            
            $code_generated = true;
            $success = "Verification code generated! <br><br><span style='font-size: 1.4rem; letter-spacing: 2px; color: #f8d76d;'><strong>$code</strong></span><br><br>Please copy this code and proceed.";
        }} else {{
            $error = "No account found with that email address.";
        }}
    }}
}}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Forgot Password - Abhinaya Institute</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
{portal_css}
        .portal-wrapper {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)), url('images/slide1.jpg.jpg') center/cover fixed; }}
    </style>
</head>
<body>
{nav_html}
<div class="portal-wrapper">
    <div class="portal-box">
        <h2>Forgot Password</h2>
        <p>Recover your student account</p>
        
        <?php if($error): ?>
            <div class="error-msg"><i class="fa fa-exclamation-circle"></i> <?php echo htmlspecialchars($error); ?></div>
        <?php endif; ?>
        
        <?php if($success): ?>
            <div class="success-msg" style="text-align: center;"><i class="fa fa-check-circle"></i> <?php echo $success; ?></div>
            <a href="reset-password.php" class="btn-submit" style="display: block; text-decoration: none; text-align: center; color: black; line-height: 20px;">Proceed to Reset Password</a>
        <?php else: ?>
            <form method="POST" action="forgot-password.php">
                <div class="form-group">
                    <label>Registered Email Address</label>
                    <input type="email" name="email" required placeholder="Enter your email" value="<?php echo htmlspecialchars($_POST['email'] ?? ''); ?>">
                </div>
                <button type="submit" class="btn-submit">Request Reset Code</button>
            </form>
        <?php endif; ?>
        
        <div class="portal-links">
            Remembered your password? <a href="login.php">Login here</a>
        </div>
    </div>
</div>
{footer_html}
</body>
</html>
"""

reset_php = f"""<?php
session_start();
require 'config.php';

if (isset($_SESSION['user_id'])) {{
    header("Location: dashboard.php");
    exit();
}}

if (!isset($_SESSION['reset_email']) || !isset($_SESSION['reset_code'])) {{
    header("Location: forgot-password.php");
    exit();
}}

$error = '';

if ($_SERVER["REQUEST_METHOD"] == "POST") {{
    $code = trim($_POST['code']);
    $password = $_POST['password'];
    $confirm_password = $_POST['confirm_password'];
    
    if (empty($code) || empty($password)) {{
        $error = "Please fill in all fields.";
    }} elseif ($code != $_SESSION['reset_code']) {{
        $error = "The verification code is incorrect.";
    }} elseif ($password !== $confirm_password) {{
        $error = "Passwords do not match.";
    }} elseif (strlen($password) < 6) {{
        $error = "Password must be at least 6 characters long.";
    }} else {{
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);
        $stmt = $pdo->prepare("UPDATE users SET password = ? WHERE email = ?");
        if ($stmt->execute([$hashed_password, $_SESSION['reset_email']])) {{
            // Clean up session
            unset($_SESSION['reset_code']);
            unset($_SESSION['reset_email']);
            unset($_SESSION['reset_time']);
            
            $_SESSION['login_success'] = "Password reset successfully! You can now log in.";
            header("Location: login.php");
            exit();
        }} else {{
            $error = "Failed to reset password. Please try again.";
        }}
    }}
}}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reset Password - Abhinaya Institute</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
{portal_css}
        .portal-wrapper {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)), url('images/slide1.jpg.jpg') center/cover fixed; }}
    </style>
</head>
<body>
{nav_html}
<div class="portal-wrapper">
    <div class="portal-box">
        <h2>Reset Password</h2>
        <p>Set a new password for <?php echo htmlspecialchars($_SESSION['reset_email']); ?></p>
        
        <?php if($error): ?>
            <div class="error-msg"><i class="fa fa-exclamation-circle"></i> <?php echo htmlspecialchars($error); ?></div>
        <?php endif; ?>
        
        <form method="POST" action="reset-password.php">
            <div class="form-group">
                <label>Verification Code</label>
                <input type="text" name="code" required placeholder="Enter the 6-digit code">
            </div>
            <div class="form-group">
                <label>New Password</label>
                <input type="password" name="password" required placeholder="Enter new password">
            </div>
            <div class="form-group">
                <label>Confirm New Password</label>
                <input type="password" name="confirm_password" required placeholder="Confirm new password">
            </div>
            <button type="submit" class="btn-submit">Reset Password</button>
        </form>
    </div>
</div>
{footer_html}
</body>
</html>
"""

# Write files
with open('c:/Xamp/htdocs/abhinaya/forgot-password.php', 'w', encoding='utf-8') as f:
    f.write(forgot_php)

with open('c:/Xamp/htdocs/abhinaya/reset-password.php', 'w', encoding='utf-8') as f:
    f.write(reset_php)

print("Generated forgot-password.php and reset-password.php")
