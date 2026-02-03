<?php
header("Cache-Control: no-cache");
header("Content-Type: text/html");

$method = $_SERVER['REQUEST_METHOD'];
$queryString = $_SERVER['QUERY_STRING'] ?? '';
$contentType = $_SERVER['CONTENT_TYPE'] ?? '';
$userAgent = $_SERVER['HTTP_USER_AGENT'] ?? 'unknown';
$ip = $_SERVER['REMOTE_ADDR'];
$hostname = gethostname();
$body = file_get_contents('php://input');

// Parse data based on method and content type
$parsed = [];
if ($method === 'GET') {
    $parsed = $_GET;
} elseif (in_array($method, ['POST', 'PUT', 'DELETE'])) {
    if (str_contains($contentType, 'application/json')) {
        $parsed = json_decode($body, true) ?? ['error' => 'Invalid JSON'];
    } else {
        parse_str($body, $parsed);
    }
}
?>
<!DOCTYPE html>
<html><head><title>Echo Request</title></head>
<body>
<h1 align="center">Echo Request</h1><hr>
<p><b>Hostname:</b> <?= $hostname ?></p>
<p><b>Date/Time:</b> <?= date('Y-m-d H:i:s') ?></p>
<p><b>User Agent:</b> <?= $userAgent ?></p>
<p><b>IP Address:</b> <?= $ip ?></p>
<hr>
<p><b>HTTP Method:</b> <?= $method ?></p>
<p><b>Content-Type:</b> <?= $contentType ?></p>
<p><b>Query String:</b> <?= $queryString ?></p>
<p><b>Message Body:</b> <?= $body ?></p>
<hr>
<h2>Parsed Data</h2>
<ul>
<?php if (!empty($parsed)):
    foreach ($parsed as $key => $value): ?>
        <li><b><?= $key ?>:</b> <?= is_array($value) ? implode(', ', $value) : $value ?></li>
    <?php endforeach;
else: ?>
    <li>No data</li>
<?php endif; ?>
</ul>
</body></html>
