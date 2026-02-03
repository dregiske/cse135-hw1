<?php
header("Cache-Control: no-cache");
header("Content-Type: text/html");
?>
<!DOCTYPE html>
<html><head><title>Hello CGI World</title></head>
<body>
<h1 align="center">Hello HTML World</h1><hr>
<p>Hello Andre!</p>
<p>This page was generated with the PHP programming language</p>
<p>This program was generated at: <?= date('Y-m-d H:i:s') ?></p>
<p>Your current IP Address is: <?= $_SERVER['REMOTE_ADDR'] ?></p>
</body></html>
