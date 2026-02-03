<?php
session_save_path('/tmp/php_sessions');
if (!is_dir('/tmp/php_sessions')) mkdir('/tmp/php_sessions');
session_name('PHP_SID');
session_start();
session_destroy();
setcookie('PHP_SID', '', time() - 3600, '/');

header("Cache-Control: no-cache");
?>
<!DOCTYPE html>
<html><head><title>State - Session Cleared</title></head>
<body>
<h1 align="center">Session Cleared</h1><hr>
<p>Your session data has been deleted.</p>
<p><a href="/cgi-bin/php/state-php-save.php">Back to Save Page</a></p>
<p><a href="/cgi-bin/php/state-php-view.php">Back to View Page</a></p>
</body></html>
