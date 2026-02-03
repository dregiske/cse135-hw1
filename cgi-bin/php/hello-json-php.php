<?php
header("Cache-Control: no-cache");
header("Content-Type: application/json");

echo json_encode([
    "greeting" => "Hello Andre!",
    "language" => "PHP",
    "generated_at" => date('Y-m-d H:i:s'),
    "ip_address" => $_SERVER['REMOTE_ADDR']
], JSON_PRETTY_PRINT);
?>
