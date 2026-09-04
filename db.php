<?php
$host = getenv('DB_HOST') ?: '127.0.0.1';
$port = getenv('DB_PORT') ? (int)getenv('DB_PORT') : 3306;
$dbname = getenv('DB_NAME') ?: 'abhinaya_db';
$user = getenv('DB_USER') ?: 'root';
$pass = getenv('DB_PASS') !== false ? getenv('DB_PASS') : '';

$conn = @mysqli_connect($host, $user, $pass, $dbname, $port);
if (!$conn) {
    die("<div style='font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 12px; background: #fff8f8; color: #991b1b; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);'>"
        . "<h3 style='margin-top:0; color:#b91c1c;'>Database Connection Error</h3>"
        . "<p>Database connection failed: " . htmlspecialchars(mysqli_connect_error()) . "</p>"
        . "<p style='font-size: 14px; color: #475569;'>If you are running on <strong>Render</strong>, please configure your cloud MySQL credentials (<code>DB_HOST</code>, <code>DB_PORT</code>, <code>DB_USER</code>, <code>DB_PASS</code>, <code>DB_NAME</code>) in the <strong>Environment</strong> tab of your Render service.</p>"
        . "</div>");
}
?>
