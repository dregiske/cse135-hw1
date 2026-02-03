<?php
header("Cache-Control: no-cache");
header("Content-Type: text/html");
?>
<!DOCTYPE html>
<html><head><title>Environment Variables</title></head>
<body><h1 align="center">Environment Variables</h1><hr>
<?php
$vars = array_merge($_SERVER, $_ENV);
ksort($vars);
foreach ($vars as $key => $value) {
    echo "<b>$key:</b> $value<br />\n";
}
?>
</body></html>
