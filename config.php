<?php
$host = getenv('DB_HOST') ?: '127.0.0.1';
$port = getenv('DB_PORT') ?: '3306';
$dbname = getenv('DB_NAME') ?: 'abhinaya_db';
$user = getenv('DB_USER') ?: 'root';
$pass = getenv('DB_PASS') !== false ? getenv('DB_PASS') : '';

$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
];

// If SSL is required or CA is provided
if (getenv('DB_SSL') === 'true' || getenv('DB_SSL_CA')) {
    if (getenv('DB_SSL_CA')) {
        $options[PDO::MYSQL_ATTR_SSL_CA] = getenv('DB_SSL_CA');
    }
    $options[PDO::MYSQL_ATTR_SSL_VERIFY_SERVER_CERT] = false;
}

try {
    $pdo = new PDO("mysql:host=$host;port=$port;dbname=$dbname;charset=utf8mb4", $user, $pass, $options);
} catch (PDOException $e) {
    die("<div style='font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 12px; background: #fff8f8; color: #991b1b; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);'>"
        . "<h3 style='margin-top:0; color:#b91c1c;'>Database Connection Error</h3>"
        . "<p>Could not connect to the database <strong>" . htmlspecialchars($dbname) . "</strong> on <strong>" . htmlspecialchars($host) . ":" . htmlspecialchars($port) . "</strong>.</p>"
        . "<p style='font-size: 13px; color: #666; background: #fee2e2; padding: 8px 12px; border-radius: 6px; font-family: monospace;'>" . htmlspecialchars($e->getMessage()) . "</p>"
        . "<p style='font-size: 14px; color: #475569;'>If you are running on <strong>Render</strong>, please add your cloud MySQL credentials (<code>DB_HOST</code>, <code>DB_PORT</code>, <code>DB_USER</code>, <code>DB_PASS</code>, <code>DB_NAME</code>) to the <strong>Environment</strong> tab in your Render dashboard.</p>"
        . "</div>");
}
?>
