<?php
session_save_path('/tmp/php_sessions');
if (!is_dir('/tmp/php_sessions')) mkdir('/tmp/php_sessions');
session_name('PHP_SID');
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $_SESSION['name'] = $_POST['name'] ?? $_SESSION['name'] ?? '';
    $_SESSION['message'] = $_POST['message'] ?? $_SESSION['message'] ?? '';
    $_SESSION['saved_at'] = date('Y-m-d H:i:s');
}

header("Cache-Control: no-cache");
?>
<!DOCTYPE html>
<html><head><title>State - Save Data</title></head>
<body>
<h1 align="center">State Demo - Save Data</h1><hr>
<form method="POST" action="/cgi-bin/php/state-php-save.php">
    <label>Name: </label><input type="text" name="name" value="<?= $_SESSION['name'] ?? '' ?>" /><br /><br />
    <label>Message: </label><input type="text" name="message" value="<?= $_SESSION['message'] ?? '' ?>" /><br /><br />
    <input type="submit" value="Save" />
</form>
<hr>
<p><a href="/cgi-bin/php/state-php-view.php">View saved data</a></p>
<p><a href="/cgi-bin/php/state-php-destroy.php">Clear session</a></p>
</body></html>
