<?php

$data = 'hello'; 
$output=shell_exec("python front.py ".$data);

echo $output;

?>