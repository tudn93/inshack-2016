<?php

session_start();

/* Handle logs files */
function get_client_ip()
{
    $ipaddress = '';
    if (getenv('HTTP_CLIENT_IP'))
        $ipaddress = getenv('HTTP_CLIENT_IP');
    else if (getenv('HTTP_X_FORWARDED_FOR'))
        $ipaddress = getenv('HTTP_X_FORWARDED_FOR');
    else if (getenv('HTTP_X_FORWARDED'))
        $ipaddress = getenv('HTTP_X_FORWARDED');
    else if (getenv('HTTP_FORWARDED_FOR'))
        $ipaddress = getenv('HTTP_FORWARDED_FOR');
    else if (getenv('HTTP_FORWARDED'))
        $ipaddress = getenv('HTTP_FORWARDED');
    else if (getenv('REMOTE_ADDR'))
        $ipaddress = getenv('REMOTE_ADDR');
    else
        $ipaddress = '-';
    return $ipaddress;
}

$LOGS_DIR = "logs/";
if (!isset($_SESSION['logfile']) || !file_exists($LOGS_DIR . $_SESSION['logfile'])) {
    $log_file = sha1(rand());
    while (file_exists($LOGS_DIR . $log_file)) {
        $log_file = sha1(rand());
    }
    $_SESSION['logfile'] = $log_file;
}
$log_file = $_SESSION['logfile'];
$current = file_get_contents($LOGS_DIR . $log_file);
$current .= get_client_ip() . ' - - [' . date(DATE_RFC2822) . '] 200 - "-" "' . $_SERVER['HTTP_USER_AGENT'] . '"' . "\n";
file_put_contents($LOGS_DIR . $log_file, $current);
/* End handle log files */


/* Handle include right file */
if (isset($_GET['p'])) {
    $page = $_GET['p'];
} else {
    $page = "home";
}
$content = "<h1>Welcome to UltraSafe's website</h1>";
$content .= "<p class='lead'>We exist to show you how security is done.</p>";
$before_content = "<div class='col-xs-12'>";
$after_content = "</div>";
if (file_exists($page . ".php")) {
    $to_include = $page . ".php";
}else if(file_exists($page) && is_file($page)) {
    // .php5 .php7 .ini extensions
    $to_include = $page;
}else{
    // the file does not exists -> 404
    $to_include = "404.php";
}
/* End handle include right file */


/****************/
/* Page content */
/****************/
?>
<html>
<head>
    <title>UltraSecure</title>
    <link rel="stylesheet" type="text/css" href="/css/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="/css/custom.css">
</head>
<body>

<script type="text/javascript" src="/css/bootstrap/js/jquery.min.js"></script>
<script type="text/javascript" src="/css/bootstrap/js/bootstrap.min.js"></script>
<nav class="navbar navbar-inverse navbar-fixed-top">
    <div class="container-fluid">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar"
                    aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/">UltraSecure</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
            <ul class="nav navbar-nav navbar-right">
                <li class="<?php if($page === "home") echo 'active'; ?>"><a href="/home/">Home</a></li>
                <li class="<?php if($page === "logfile") echo 'active'; ?>"><a href="/logfile/">Log File</a></li>
                <li class="<?php if($page === "article") echo 'active'; ?>"><a href="/article/">News</a></li>
                <li class="<?php if($page === "contact") echo 'active'; ?>"><a href="/contact/">Contact</a></li>
            </ul>
        </div>
    </div>
</nav>

<div id="background-container">
    <div class="container">
        <div class="jumbotron">
            <?php echo $content; ?>
        </div>
        <div class="box">
            <div class="row">
                <?php
                echo $before_content;
                include_once($to_include);
                echo $after_content;
                ?>
            </div>
        </div>
    </div>
</div>

</body>
</html>
