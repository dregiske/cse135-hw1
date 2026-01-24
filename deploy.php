<?php
// GitHub webhook secret
$secret = "cse135_deploy_secret_2026";

// Get the POST payload from GitHub
$payload = file_get_contents('php://input');

// Get the signature from GitHub
$received_signature = $_SERVER['HTTP_X_HUB_SIGNATURE_256'] ?? '';

// Calculate expected signature
$expected_signature = 'sha256=' . hash_hmac('sha256', $payload, $secret);

// Verify the signature matches
if (!hash_equals($expected_signature, $received_signature)) {
    http_response_code(403);
    die('Invalid signature - webhook rejected');
}

// Signature is valid, execute the deploy script
$output = shell_exec('/home/grader/deploy.sh 2>&1');

// Log the deployment
$log_message = date('Y-m-d H:i:s') . " - Webhook triggered successfully\n";
$log_message .= "Output: " . $output . "\n\n";
file_put_contents('/home/grader/webhook.log', $log_message, FILE_APPEND);

// Send response to GitHub
http_response_code(200);
echo "Deployment triggered successfully!";
?>
