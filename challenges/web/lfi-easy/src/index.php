<?php
// FLAG{Leak_of_Flag_is_Impossible=LFI}
?>
<!DOCTYPE html>
<html>
<head>
	<title>LFI</title>
	<link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
<div class="page">
	<a href="?page=kikoo.php">Kikoos</a>
	<a href="?page=cars.php">CARS</a>
	<h1>Welcome into my H0me &lt;3</h1>
	<?php 
		if(isset($_GET['page'])){
			$page = $_GET['page'];
		}else{
			$page = 'cars.php';
		}
		if(is_string($page)){
			if($page[0] === '/' || strpos($page, '..') !== false){
				echo 'Sorry, you can\'t do that :/';
				die(0);
			}
			include_once($page);
		}
	?>
</div>
</body>
</html>