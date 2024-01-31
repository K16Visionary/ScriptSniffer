<?php
$pythonScriptPath = 'main.py';
$output = shell_exec("python3 $pythonScriptPath");

echo json_encode(['output' => $output]);
?>
