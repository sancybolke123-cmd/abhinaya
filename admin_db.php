<?php
session_start();
require 'config.php';

// Simple passcode for admin dashboard (default: admin123, can be changed via ADMIN_PIN env)
$admin_pin = getenv('ADMIN_PIN') ?: 'admin123';
$authenticated = false;

if (isset($_SESSION['admin_auth']) && $_SESSION['admin_auth'] === true) {
    $authenticated = true;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['pin'])) {
    if ($_POST['pin'] === $admin_pin) {
        $_SESSION['admin_auth'] = true;
        $authenticated = true;
    } else {
        $pin_error = "Invalid passcode. Please try again.";
    }
}

if (isset($_GET['logout'])) {
    unset($_SESSION['admin_auth']);
    header("Location: admin_db.php");
    exit();
}

// Fetch tables data if authenticated
$users = [];
$payments = [];
$contacts = [];

if ($authenticated) {
    try {
        $stmt = $pdo->query("SELECT id, full_name, email, course, created_at FROM users ORDER BY id DESC");
        $users = $stmt->fetchAll();
    } catch (Exception $e) {}

    try {
        $stmt = $pdo->query("SELECT id, full_name, email, course, amount, txn_id, utr_number, payment_method, screenshot_path, status, payment_receipt, created_at FROM payments ORDER BY id DESC");
        $payments = $stmt->fetchAll();
    } catch (Exception $e) {}

    try {
        $stmt = $pdo->query("SELECT id, name, email, phone, message, submitted_at FROM contacts ORDER BY id DESC");
        $contacts = $stmt->fetchAll();
    } catch (Exception $e) {}
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Database Manager - Abhinaya Institute</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; background: #0a0a0a; color: #f1f5f9; min-height: 100vh; padding: 30px 20px; }
        .container { max-width: 1200px; margin: auto; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(212, 175, 55, 0.2); padding-bottom: 20px; margin-bottom: 30px; }
        .logo-title { font-family: 'Cinzel', serif; font-size: 1.8rem; color: #d4af37; font-weight: 700; }
        .logo-title span { font-size: 0.95rem; color: #94a3b8; font-family: 'Poppins', sans-serif; display: block; font-weight: 400; }
        
        .btn-nav { display: inline-flex; align-items: center; gap: 8px; background: rgba(212, 175, 55, 0.15); color: #d4af37; border: 1px solid rgba(212, 175, 55, 0.3); padding: 8px 16px; border-radius: 8px; text-decoration: none; font-size: 0.9rem; transition: 0.3s; }
        .btn-nav:hover { background: #d4af37; color: #000; }
        
        /* PIN Login Card */
        .login-card { max-width: 420px; margin: 80px auto; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(212, 175, 55, 0.3); padding: 35px; border-radius: 16px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .login-card h2 { font-family: 'Cinzel', serif; color: #d4af37; margin-bottom: 10px; font-size: 1.5rem; }
        .login-card p { color: #94a3b8; font-size: 0.9rem; margin-bottom: 25px; }
        .pin-input { width: 100%; padding: 14px; background: rgba(0,0,0,0.5); border: 1px solid #334155; border-radius: 8px; color: white; font-size: 1.1rem; text-align: center; letter-spacing: 2px; margin-bottom: 15px; }
        .pin-input:focus { outline: none; border-color: #d4af37; }
        .btn-submit { width: 100%; padding: 14px; background: linear-gradient(135deg, #d4af37, #aa820a); border: none; border-radius: 8px; color: #000; font-weight: 600; font-size: 1rem; cursor: pointer; transition: 0.3s; }
        .btn-submit:hover { opacity: 0.9; transform: translateY(-2px); }
        .error-msg { background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; color: #fca5a5; padding: 10px; border-radius: 8px; font-size: 0.85rem; margin-bottom: 15px; }

        /* Stats Cards */
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; display: flex; align-items: center; gap: 15px; }
        .stat-icon { width: 50px; height: 50px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; }
        .icon-users { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
        .icon-payments { background: rgba(34, 197, 94, 0.15); color: #4ade80; }
        .icon-contacts { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
        .stat-info h4 { font-size: 0.85rem; color: #94a3b8; font-weight: 400; }
        .stat-info .stat-num { font-size: 1.6rem; font-weight: 700; color: #fff; }

        /* Tabs */
        .tab-bar { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; }
        .tab-btn { background: transparent; border: none; color: #94a3b8; font-size: 1rem; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-family: 'Poppins', sans-serif; transition: 0.3s; display: flex; align-items: center; gap: 8px; }
        .tab-btn.active { background: rgba(212, 175, 55, 0.15); color: #d4af37; font-weight: 600; border: 1px solid rgba(212, 175, 55, 0.3); }
        .tab-btn:hover:not(.active) { color: #fff; background: rgba(255,255,255,0.05); }

        /* Tables */
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .table-wrap { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th { background: rgba(255, 255, 255, 0.05); color: #d4af37; padding: 14px 18px; font-weight: 600; font-size: 0.9rem; border-bottom: 1px solid rgba(255,255,255,0.1); }
        td { padding: 14px 18px; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.9rem; color: #cbd5e1; }
        tr:hover td { background: rgba(212, 175, 55, 0.03); }
        .badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; background: rgba(212,175,55,0.15); color: #d4af37; }
        .empty-row { text-align: center; padding: 40px; color: #64748b; font-style: italic; }
    </style>
</head>
<body>

<div class="container">
    <?php if (!$authenticated): ?>
        <div class="login-card">
            <i class="fa-solid fa-database" style="font-size: 2.5rem; color: #d4af37; margin-bottom: 15px;"></i>
            <h2>Database Access</h2>
            <p>Enter the master passcode to inspect your live database records.</p>
            
            <?php if (!empty($pin_error)): ?>
                <div class="error-msg"><?php echo htmlspecialchars($pin_error); ?></div>
            <?php endif; ?>

            <form method="POST">
                <input type="password" name="pin" class="pin-input" placeholder="Passcode (default: admin123)" required autofocus>
                <button type="submit" class="btn-submit"><i class="fa-solid fa-lock-open"></i> Unlock Database</button>
            </form>
            <div style="margin-top: 20px;">
                <a href="home.html" style="color: #64748b; font-size: 0.85rem; text-decoration: none;"><i class="fa-solid fa-arrow-left"></i> Back to Home</a>
            </div>
        </div>
    <?php else: ?>
        <div class="header">
            <div class="logo-title">
                Abhinaya Database Manager
                <span>Live MySQL Database Inspection & Records</span>
            </div>
            <div style="display: flex; gap: 10px;">
                <a href="home.html" class="btn-nav"><i class="fa-solid fa-house"></i> Website</a>
                <a href="admin_db.php?logout=1" class="btn-nav" style="border-color: #ef4444; color: #ef4444;"><i class="fa-solid fa-right-from-bracket"></i> Lock</a>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon icon-users"><i class="fa-solid fa-users"></i></div>
                <div class="stat-info">
                    <h4>Registered Students</h4>
                    <div class="stat-num"><?php echo count($users); ?></div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon icon-payments"><i class="fa-solid fa-receipt"></i></div>
                <div class="stat-info">
                    <h4>Payment Receipts</h4>
                    <div class="stat-num"><?php echo count($payments); ?></div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon icon-contacts"><i class="fa-solid fa-envelope"></i></div>
                <div class="stat-info">
                    <h4>Contact Inquiries</h4>
                    <div class="stat-num"><?php echo count($contacts); ?></div>
                </div>
            </div>
        </div>

        <div class="tab-bar">
            <button class="tab-btn active" onclick="switchTab('tab-users')"><i class="fa-solid fa-users"></i> Users (<?php echo count($users); ?>)</button>
            <button class="tab-btn" onclick="switchTab('tab-payments')"><i class="fa-solid fa-receipt"></i> Payments (<?php echo count($payments); ?>)</button>
            <button class="tab-btn" onclick="switchTab('tab-contacts')"><i class="fa-solid fa-envelope"></i> Contacts (<?php echo count($contacts); ?>)</button>
        </div>

        <!-- Users Tab -->
        <div id="tab-users" class="tab-content active">
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Full Name</th>
                            <th>Email Address</th>
                            <th>Enrolled Course</th>
                            <th>Registration Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php if (empty($users)): ?>
                            <tr><td colspan="5" class="empty-row">No registered users yet.</td></tr>
                        <?php else: ?>
                            <?php foreach ($users as $u): ?>
                                <tr>
                                    <td>#<?php echo htmlspecialchars($u['id']); ?></td>
                                    <td><strong><?php echo htmlspecialchars($u['full_name']); ?></strong></td>
                                    <td><?php echo htmlspecialchars($u['email']); ?></td>
                                    <td><span class="badge"><?php echo htmlspecialchars($u['course'] ?: 'Not Specified'); ?></span></td>
                                    <td><?php echo htmlspecialchars($u['created_at']); ?></td>
                                </tr>
                            <?php endforeach; ?>
                        <?php endif; ?>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Payments Tab -->
        <div id="tab-payments" class="tab-content">
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Student Name</th>
                            <th>Email</th>
                            <th>Course</th>
                            <th>Amount</th>
                            <th>UPI UTR / Ref No</th>
                            <th>Payment Mode</th>
                            <th>Proof / Screenshot</th>
                            <th>Receipt File</th>
                            <th>Payment Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php if (empty($payments)): ?>
                            <tr><td colspan="10" class="empty-row">No payment records found.</td></tr>
                        <?php else: ?>
                            <?php foreach ($payments as $p): ?>
                                <tr>
                                    <td>#<?php echo htmlspecialchars($p['id']); ?></td>
                                    <td><strong><?php echo htmlspecialchars($p['full_name']); ?></strong></td>
                                    <td><?php echo htmlspecialchars($p['email']); ?></td>
                                    <td><span class="badge"><?php echo htmlspecialchars($p['course']); ?></span></td>
                                    <td><strong style="color: #4ade80;">₹<?php echo htmlspecialchars($p['amount'] ?? '0'); ?></strong></td>
                                    <td><code style="color: #60a5fa; font-size: 0.85rem; background: rgba(59,130,246,0.1); padding: 2px 6px; border-radius: 4px;"><?php echo htmlspecialchars($p['utr_number'] ?: 'N/A'); ?></code></td>
                                    <td><?php echo htmlspecialchars($p['payment_method'] ?? 'UPI'); ?></td>
                                    <td>
                                        <?php if (!empty($p['screenshot_path'])): ?>
                                            <a href="<?php echo htmlspecialchars($p['screenshot_path']); ?>" target="_blank" style="color: #fbbf24; text-decoration: underline;"><i class="fa fa-image"></i> View Proof</a>
                                        <?php else: ?>
                                            <span style="color: #64748b;">None</span>
                                        <?php endif; ?>
                                    </td>
                                    <td>
                                        <?php if (!empty($p['payment_receipt'])): ?>
                                            <a href="<?php echo htmlspecialchars($p['payment_receipt']); ?>" target="_blank" style="color: #60a5fa; text-decoration: underline;"><i class="fa fa-file-invoice"></i> Receipt</a>
                                        <?php else: ?>
                                            N/A
                                        <?php endif; ?>
                                    </td>
                                    <td><?php echo htmlspecialchars($p['created_at']); ?></td>
                                </tr>
                            <?php endforeach; ?>
                        <?php endif; ?>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Contacts Tab -->
        <div id="tab-contacts" class="tab-content">
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Message</th>
                            <th>Submitted At</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php if (empty($contacts)): ?>
                            <tr><td colspan="6" class="empty-row">No contact inquiries found.</td></tr>
                        <?php else: ?>
                            <?php foreach ($contacts as $c): ?>
                                <tr>
                                    <td>#<?php echo htmlspecialchars($c['id']); ?></td>
                                    <td><strong><?php echo htmlspecialchars($c['name']); ?></strong></td>
                                    <td><?php echo htmlspecialchars($c['email']); ?></td>
                                    <td><?php echo htmlspecialchars($c['phone'] ?: 'N/A'); ?></td>
                                    <td style="max-width: 350px;"><?php echo htmlspecialchars($c['message']); ?></td>
                                    <td><?php echo htmlspecialchars($c['submitted_at']); ?></td>
                                </tr>
                            <?php endforeach; ?>
                        <?php endif; ?>
                    </tbody>
                </table>
            </div>
        </div>
    <?php endif; ?>
</div>

<script>
function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    event.currentTarget.classList.add('active');
}
</script>

</body>
</html>
