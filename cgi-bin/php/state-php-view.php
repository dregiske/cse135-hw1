<?php
session_save_path('/tmp/php_sessions');
if (!is_dir('/tmp/php_sessions')) mkdir('/tmp/php_sessions');
session_name('PHP_SID');
session_start();

header("Cache-Control: no-cache");
?>
<!DOCTYPE html>
<html><head><title>State - View Data</title></head>
<body>
<h1 align="center">State Demo - View Data</h1><hr>
<?php if (isset($_SESSION['name'])): ?>
    <p><b>Name:</b> <?= $_SESSION['name'] ?></p>
    <p><b>Message:</b> <?= $_SESSION['message'] ?></p>
    <p><b>Saved at:</b> <?= $_SESSION['saved_at'] ?></p>
<?php else: ?>
    <p>No data saved yet. Go save some!</p>
<?php endif; ?>
<hr>
<p><a href="/cgi-bin/php/state-php-save.php">Go back and edit</a></p>
<p><a href="/cgi-bin/php/state-php-destroy.php">Clear session</a></p>
</body></html>
