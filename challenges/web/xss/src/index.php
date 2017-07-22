<?php
	session_start();
	if(isset($_GET['f']) && file_exists('tmp/'.$_GET['f'])){
		echo file_get_contents('tmp/'.$_GET['f']);
		die(0);
	}
	if(isset($_GET['vote']) && isset($_GET['number']) && isset($_GET['type'])){
		$vote = (string)$_GET['vote'];
		$type = (string)$_GET['type'];
		$number = (string)$_GET['number'];
		if( ($vote === "ninja" || $vote === "burger")
			&& ($type === "plus" || $type === "minus")
			&& ($number === "1" || $number === "2" || $number === "3")) {
				$key = "score_" . $vote . "_" . $number;
				if(! isset($_SESSION[$key])){
					$_SESSION[$key] = 0;
				}
				if($type === "plus"){
					$_SESSION[$key] = (int)($_SESSION[$key]) + 1;
				}else{
					$_SESSION[$key] = (int)($_SESSION[$key]) - 1;					
				}
				header( 'Location: /' ) ;
				die(0);
			}
	}
?>

<!DOCTYPE html>
<html>
<head>
	<title>Burger-Ninja</title>
	<link rel="stylesheet" type="text/css" href="css/bootstrap/css/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="css/custom.css">
</head>
<body>
<div id="background-container">
	<div class="container">

		<div class="jumbotron">
			<h1>Welcome to Burger-Ninja !</h1>
				<p class="lead">Please vote for your favourite Burger and/or Ninja bellow :)</p>
				<p class="lead">If you really admire what we do here, please leave <a href="#leave-comment">a comment</a>. An admin will read it as soon as possible.</p>
		</div>


		<div class="box">
			<div class="row">
				<div class="col-md-4">
					<img src="img/ninja1.jpeg" class="img img-responsive">
					<div class="row voting">
						<a class="col-xs-2 col-xs-offset-3 circle-green text-center" href="?vote=ninja&number=1&type=plus">
							<i class="glyphicon glyphicon-thumbs-up"></i>
						</a>
						<a class="col-xs-2  col-xs-offset-2 circle-red text-center" href="?vote=ninja&number=1&type=minus">
							<i class="glyphicon glyphicon-thumbs-down"></i>
						</a>
					</div>
					<div class="row score">
						<div class="col-md-4 col-md-offset-4">
							<button class="btn btn-warning" type="button">
								<b>Score</b> <span class="badge"><?php 
									if(isset($_SESSION['score_ninja_1']))
									{
										echo 61 + (int)($_SESSION['score_ninja_1']);
									}else{
										echo 61;
									}
								 ?> </span>
							</button>
						</div>
					</div>
				</div>
				<div class="col-md-4">
					<img src="img/ninja2.jpeg" class="img img-responsive">
					<div class="row voting">
						<a class="col-xs-2 col-xs-offset-3 circle-green text-center" href="?vote=ninja&number=2&type=plus">
							<i class="glyphicon glyphicon-thumbs-up"></i>
						</a>
						<a class="col-xs-2  col-xs-offset-2 circle-red text-center" href="?vote=ninja&number=2&type=minus">
							<i class="glyphicon glyphicon-thumbs-down"></i>
						</a>
					</div>
					<div class="row score">
						<div class="col-md-4 col-md-offset-4">
							<button class="btn btn-warning" type="button">
								<b>Score</b> <span class="badge"><?php 
									if(isset($_SESSION['score_ninja_2']))
									{
										echo 35 + (int)($_SESSION['score_ninja_2']);
									}else{
										echo 35;
									}
								 ?> </span>
							</button>
						</div>
					</div>
				</div>
				<div class="col-md-4">
					<img src="img/ninja3.jpeg" class="img img-responsive">
					<div class="row voting">
						<a class="col-xs-2 col-xs-offset-3 circle-green text-center" href="?vote=ninja&number=3&type=plus">
							<i class="glyphicon glyphicon-thumbs-up"></i>
						</a>
						<a class="col-xs-2  col-xs-offset-2 circle-red text-center" href="?vote=ninja&number=3&type=minus">
							<i class="glyphicon glyphicon-thumbs-down"></i>
						</a>
					</div>
					<div class="row score">
						<div class="col-md-4 col-md-offset-4">
							<button class="btn btn-warning" type="button">
								<b>Score</b> <span class="badge"><?php 
									if(isset($_SESSION['score_ninja_3']))
									{
										echo 107 + (int)($_SESSION['score_ninja_3']);
									}else{
										echo 107;
									}
								 ?> </span>
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>


		<div class="box">
			<div class="row">
				<div class="col-md-4">
					<img src="img/burger1.jpg" class="img img-responsive">
					<div class="row voting">
						<a class="col-xs-2 col-xs-offset-3 circle-green text-center" href="?vote=burger&number=1&type=plus">
							<i class="glyphicon glyphicon-thumbs-up"></i>
						</a>
						<a class="col-xs-2  col-xs-offset-2 circle-red text-center" href="?vote=burger&number=1&type=minus">
							<i class="glyphicon glyphicon-thumbs-down"></i>
						</a>
					</div>
					<div class="row score">
						<div class="col-md-4 col-md-offset-4">
							<button class="btn btn-warning" type="button">
								<b>Score</b> <span class="badge"><?php 
									if(isset($_SESSION['score_burger_1']))
									{
										echo 82 + (int)($_SESSION['score_burger_1']);
									}else{
										echo 82;
									}
								 ?> </span>
							</button>
						</div>
					</div>
				</div>
				<div class="col-md-4">
					<img src="img/burger2.jpg" class="img img-responsive">
					<div class="row voting">
						<a class="col-xs-2 col-xs-offset-3 circle-green text-center" href="?vote=burger&number=2&type=plus">
							<i class="glyphicon glyphicon-thumbs-up"></i>
						</a>
						<a class="col-xs-2  col-xs-offset-2 circle-red text-center" href="?vote=burger&number=2&type=minus">
							<i class="glyphicon glyphicon-thumbs-down"></i>
						</a>
					</div>
					<div class="row score">
						<div class="col-md-4 col-md-offset-4">
							<button class="btn btn-warning" type="button">
								<b>Score</b> <span class="badge"><?php 
									if(isset($_SESSION['score_burger_2']))
									{
										echo 21 + (int)($_SESSION['score_burger_2']);
									}else{
										echo 21;
									}
								 ?> </span>
							</button>
						</div>
					</div>
				</div>
				<div class="col-md-4">
					<img src="img/burger3.jpeg" class="img img-responsive">
					<div class="row voting">
						<a class="col-xs-2 col-xs-offset-3 circle-green text-center" href="?vote=burger&number=3&type=plus">
							<i class="glyphicon glyphicon-thumbs-up"></i>
						</a>
						<a class="col-xs-2  col-xs-offset-2 circle-red text-center" href="?vote=burger&number=3&type=minus">
							<i class="glyphicon glyphicon-thumbs-down"></i>
						</a>
					</div>
					<div class="row score">
						<div class="col-md-4 col-md-offset-4">
							<button class="btn btn-warning" type="button">
								<b>Score</b> <span class="badge"><?php 
									if(isset($_SESSION['score_burger_3']))
									{
										echo 5978 + (int)($_SESSION['score_burger_3']);
									}else{
										echo 5978;
									}
								 ?> </span>
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>


	<?php
		if(isset($_POST['submit']) && $_POST['submit'] === 'Submit message'
			&& isset($_POST['content']) && isset($_POST['title']))
		{
			$file_path = 'tmp/' . time() . sha1(rand()) . '.html';
			while(file_exists($file_path))
			{
				$file_path = 'tmp/' . time() . sha1(rand()) . '.html';
			}
			$xss_file = fopen($file_path, "w");
			$message_to_add = '<h3>' . htmlentities($_POST['title']) . '</h3>' . "<p>" . $_POST['content'] . "<br></p>";
			fwrite($xss_file, $message_to_add);
			fclose($xss_file);
			$_SESSION["files"][] = $file_path;
		}
		if(isset($_SESSION["files"]))
		{ ?>
		<div class="box">
			<div class="row">
				<div class="col-xs-12">
				<?php
					echo '<h2>Your comments : </h2>';
					$count = 0;
					foreach ($_SESSION["files"] as $key => $file_path) {
						if(!is_string($file_path) || $file_path === '' ){
							unset($_SESSION["files"][$key]);
						}else{
							if(!file_exists($file_path)){
								unset($_SESSION["files"][$key]);
							}else{
							?>
							<div class="box row">
								<div class="col-xs-12" style="font-size: ">
									<?php
										echo file_get_contents($file_path);
										$count++ ;
									?>
									<p>
									<small>Awaiting admin moderation..</small>
									</p>
								</div>
							</div>
							<?php
							}
						}
					}
					if($count === 0){
						echo '<p>The admin read all your messages, and decided to delete them all, because they weren\'t "burger-friendly". Have a nice day ;).</p>';
					}
				?>
				</div>
			</div>
		</div>
		<?php } ?>

		<div class="row box">
			<div class="col-xs-12 form" id="leave-comment">
				<h2>Post your comment bellow : </h2>
				<form method="POST" action="">
					<label class="sr-only" for="title">Post Title :</label>
					<input id="title" name="title" class="form-control" type="text" placeholder="Your Title" required="">
					<label class="sr-only" for="content">Content</label>
					<textarea class="form-control" id="content" name="content" type="textarea" placeholder="Your content" required=""></textarea>
					<input type="submit" class="btn btn-lg btn-success btn-block" name="submit" value="Submit message">
				</form>
			</div>
		</div>

	</div>
</div>
</body>
</html>