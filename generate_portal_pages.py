import re

with open('c:/Xamp/htdocs/abhinaya/home.html', 'r', encoding='utf-8') as f:
    home = f.read()

nav_match = re.search(r'<nav>.*?</nav>', home, re.DOTALL)
footer_match = re.search(r'<footer[^>]*>.*?</footer>', home, re.DOTALL)

# Since we are renaming student-portal.html to .php, update the nav html
nav_html = nav_match.group(0) if nav_match else ''
nav_html = nav_html.replace('student-portal.html', 'student-portal.php')

footer_html = footer_match.group(0) if footer_match else ''

# 1. config.php
config_php = """<?php
$host = '127.0.0.1';
$dbname = 'abhinaya_db';
$user = 'root';
$pass = '';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Could not connect to the database $dbname :" . $e->getMessage());
}
?>
"""

# 2. setup_database.php
setup_database_php = """<?php
$host = '127.0.0.1';
$user = 'root';
$pass = '';

try {
    $pdo = new PDO("mysql:host=$host", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Create database if not exists
    $pdo->exec("CREATE DATABASE IF NOT EXISTS abhinaya_db");
    echo "Database created or already exists.<br>";
    
    // Switch to database
    $pdo->exec("USE abhinaya_db");
    
    // Create users table
    $sql = "CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        full_name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )";
    $pdo->exec($sql);
    echo "Table 'users' created or already exists.<br>";

} catch (PDOException $e) {
    die("DB ERROR: " . $e->getMessage());
}
?>
"""

# CSS for all portal forms
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
        .form-group input { width: 100%; padding: 15px; border-radius: 8px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2); color: white; font-family: 'Poppins', sans-serif; font-size: 1rem; outline: none; transition: 0.3s; }
        .form-group input:focus { border-color: #d4af37; background: rgba(212,175,55,0.05); }
        
        .btn-submit { width: 100%; background: linear-gradient(135deg, #d4af37, #f8d76d); color: #0a0a0a; border: none; padding: 15px; font-size: 1.1rem; font-weight: 600; border-radius: 50px; cursor: pointer; transition: transform 0.3s, box-shadow 0.3s; margin-top: 10px; }
        .btn-submit:hover { transform: scale(1.02); box-shadow: 0 8px 20px rgba(212,175,55,0.4); }
        
        .error-msg { color: #ff6b6b; background: rgba(255,107,107,0.1); padding: 10px; border-radius: 5px; margin-bottom: 20px; border-left: 3px solid #ff6b6b; text-align: left; font-size: 0.9rem; }
        .success-msg { color: #4cd137; background: rgba(76,209,55,0.1); padding: 10px; border-radius: 5px; margin-bottom: 20px; border-left: 3px solid #4cd137; text-align: left; font-size: 0.9rem; }
        
        .portal-links { margin-top: 25px; font-size: 0.95rem; color: #aaa; }
        .portal-links a { color: #d4af37; text-decoration: none; font-weight: 500; transition: 0.3s; }
        .portal-links a:hover { color: #f8d76d; text-decoration: underline; }
"""

# 3. student-portal.php
student_portal_php = f"""<?php
session_start();
if (isset($_SESSION['user_id'])) {{
    header("Location: dashboard.php");
    exit();
}}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Portal - Abhinaya Institute</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
{portal_css}
        .portal-wrapper {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)), url('images/Bharatanatyam Dance - Indian Dance.jpg') center/cover; }}
    </style>
</head>
<body>
{nav_html}
<div class="portal-wrapper">
    <div class="portal-box">
        <i class="fa fa-graduation-cap" style="font-size: 3rem; color: #d4af37; margin-bottom: 15px;"></i>
        <h2>Student Portal</h2>
        <p>Welcome to the Abhinaya Institute Student Portal. Please login to access your dashboard, courses, and examination materials.</p>
        <a href="login.php" class="btn-submit" style="display: block; text-decoration: none; margin-bottom: 15px;">Login to Portal</a>
        <a href="register.php" class="btn-submit" style="display: block; text-decoration: none; background: transparent; border: 2px solid #d4af37; color: #d4af37; box-shadow: none;">Create New Account</a>
    </div>
</div>
{footer_html}
</body>
</html>
"""

# 4. login.php
login_php = f"""<?php
session_start();
require 'config.php';

if (isset($_SESSION['user_id'])) {{
    header("Location: dashboard.php");
    exit();
}}

$error = '';

if ($_SERVER["REQUEST_METHOD"] == "POST") {{
    $email = trim($_POST['email']);
    $password = $_POST['password'];
    
    if (empty($email) || empty($password)) {{
        $error = "Please enter both email and password.";
    }} else {{
        $stmt = $pdo->prepare("SELECT id, full_name, password FROM users WHERE email = ?");
        $stmt->execute([$email]);
        $user = $stmt->fetch();
        
        if ($user && password_verify($password, $user['password'])) {{
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['user_name'] = $user['full_name'];
            header("Location: dashboard.php");
            exit();
        }} else {{
            $error = "Invalid email or password.";
        }}
    }}
}}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Abhinaya Institute</title>
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
        <h2>Welcome Back</h2>
        <p>Sign in to continue your journey</p>
        
        <?php if($error): ?>
            <div class="error-msg"><i class="fa fa-exclamation-circle"></i> <?php echo htmlspecialchars($error); ?></div>
        <?php endif; ?>
        
        <form method="POST" action="login.php">
            <div class="form-group">
                <label>Email Address</label>
                <input type="email" name="email" required placeholder="Enter your email">
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" required placeholder="Enter your password">
            </div>
            <button type="submit" class="btn-submit">Login</button>
        </form>
        
        <div class="portal-links">
            Don't have an account? <a href="register.php">Register here</a>
        </div>
    </div>
</div>
{footer_html}
</body>
</html>
"""

# 5. register.php
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
    
    if (empty($fullname) || empty($email) || empty($password)) {{
        $error = "Please fill in all required fields.";
    }} elseif ($password !== $confirm_password) {{
        $error = "Passwords do not match.";
    }} elseif (strlen($password) < 6) {{
        $error = "Password must be at least 6 characters long.";
    }} else {{
        // Check if email exists
        $stmt = $pdo->prepare("SELECT id FROM users WHERE email = ?");
        $stmt->execute([$email]);
        if ($stmt->rowCount() > 0) {{
            $error = "Email address is already registered.";
        }} else {{
            // Insert new user
            $hashed_password = password_hash($password, PASSWORD_DEFAULT);
            $stmt = $pdo->prepare("INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)");
            if ($stmt->execute([$fullname, $email, $hashed_password])) {{
                $success = "Registration successful! You can now <a href='login.php' style='color:#fff;text-decoration:underline;'>Login here</a>.";
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
    </style>
</head>
<body>
{nav_html}
<div class="portal-wrapper">
    <div class="portal-box">
        <h2>Join Abhinaya</h2>
        <p>Create your student account</p>
        
        <?php if($error): ?>
            <div class="error-msg"><i class="fa fa-exclamation-circle"></i> <?php echo htmlspecialchars($error); ?></div>
        <?php endif; ?>
        <?php if($success): ?>
            <div class="success-msg"><i class="fa fa-check-circle"></i> <?php echo $success; ?></div>
        <?php endif; ?>
        
        <form method="POST" action="register.php">
            <div class="form-group">
                <label>Full Name</label>
                <input type="text" name="full_name" required placeholder="Enter your full name" value="<?php echo htmlspecialchars($_POST['full_name'] ?? ''); ?>">
            </div>
            <div class="form-group">
                <label>Email Address</label>
                <input type="email" name="email" required placeholder="Enter your email" value="<?php echo htmlspecialchars($_POST['email'] ?? ''); ?>">
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" required placeholder="Create a password">
            </div>
            <div class="form-group">
                <label>Confirm Password</label>
                <input type="password" name="confirm_password" required placeholder="Confirm your password">
            </div>
            <button type="submit" class="btn-submit">Register</button>
        </form>
        
        <div class="portal-links">
            Already have an account? <a href="login.php">Login here</a>
        </div>
    </div>
</div>
{footer_html}
</body>
</html>
"""

# 6. dashboard.php
dashboard_php = f"""<?php
session_start();
if (!isset($_SESSION['user_id'])) {{
    header("Location: login.php");
    exit();
}}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Abhinaya Institute</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
{portal_css}
        .portal-wrapper {{ background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), url('images/slide3.jpg.jpg') center/cover fixed; align-items: flex-start; padding-top: 150px; }}
        .dashboard-box {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(212,175,55,0.2); padding: 40px; border-radius: 15px; width: 100%; max-width: 900px; text-align: left; }}
        .dash-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 20px; }}
        .dash-header h2 {{ font-family: 'Cinzel', serif; font-size: 2rem; color: #d4af37; margin: 0; }}
        .dash-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; }}
        .dash-card {{ background: rgba(0,0,0,0.5); border-left: 4px solid #d4af37; padding: 30px; border-radius: 10px; transition: 0.3s; }}
        .dash-card:hover {{ transform: translateY(-5px); background: rgba(212,175,55,0.05); }}
        .dash-card i {{ font-size: 2rem; color: #d4af37; margin-bottom: 15px; }}
        .dash-card h4 {{ color: white; margin-bottom: 10px; font-size: 1.2rem; }}
        .dash-card p {{ color: #aaa; font-size: 0.95rem; margin-bottom: 15px; }}
        .dash-card a {{ color: #f8d76d; text-decoration: none; font-weight: 500; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }}
        .dash-card a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
{nav_html}
<div class="portal-wrapper">
    <div class="dashboard-box">
        <div class="dash-header">
            <div>
                <h2>Welcome, <?php echo htmlspecialchars($_SESSION['user_name']); ?></h2>
                <p style="color: #aaa; margin-top: 5px;">Student Dashboard</p>
            </div>
            <a href="logout.php" class="btn-submit" style="width: auto; padding: 10px 25px; margin: 0; background: transparent; border: 2px solid #d4af37; color: #d4af37;">Logout</a>
        </div>
        
        <div class="dash-grid">
            <div class="dash-card">
                <i class="fa fa-book"></i>
                <h4>My Courses</h4>
                <p>Access your enrolled Bharatanatyam batches and learning materials.</p>
                <a href="#">View Courses &rarr;</a>
            </div>
            <div class="dash-card">
                <i class="fa fa-file-text-o"></i>
                <h4>Examinations</h4>
                <p>Download previous question papers and view marksheet structures.</p>
                <a href="examinations.html">View Exams &rarr;</a>
            </div>
            <div class="dash-card">
                <i class="fa fa-calendar"></i>
                <h4>Attendance</h4>
                <p>Check your monthly class attendance and upcoming schedules.</p>
                <a href="#">View Schedule &rarr;</a>
            </div>
        </div>
    </div>
</div>
{footer_html}
</body>
</html>
"""

# 7. logout.php
logout_php = """<?php
session_start();
session_unset();
session_destroy();
header("Location: student-portal.php");
exit();
?>
"""

files = {
    'c:/Xamp/htdocs/abhinaya/config.php': config_php,
    'c:/Xamp/htdocs/abhinaya/setup_database.php': setup_database_php,
    'c:/Xamp/htdocs/abhinaya/student-portal.php': student_portal_php,
    'c:/Xamp/htdocs/abhinaya/login.php': login_php,
    'c:/Xamp/htdocs/abhinaya/register.php': register_php,
    'c:/Xamp/htdocs/abhinaya/dashboard.php': dashboard_php,
    'c:/Xamp/htdocs/abhinaya/logout.php': logout_php,
}

for filepath, content in files.items():
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Generated all backend files perfectly.")
