<h2>Please leave us a message bellow</h2>

<form method="POST" action="" id="contact-form">
	<label class="sr-only" for="title">Subject :</label>
	<input id="title" name="title" class="form-control" type="text" placeholder="Subject" required="" autofocus="">
	<label class="sr-only" for="email">Email :</label>
	<input id="email" name="email" class="form-control" type="email" placeholder="Email" required="">
	<label class="sr-only" for="content">Content :</label>
	<textarea class="form-control" id="content" name="content" type="textarea" placeholder="Your message content" required=""></textarea>
	<input type="submit" class="btn btn-lg btn-primary btn-block" name="submit" value="Submit message">
</form>

<div id="retour"></div>

<script type="text/javascript">
	$( document ).ready(function() {
		$('#contact-form').on('submit', function(event){
			$('#retour').html('<div class="alert alert-success alert-dismissible fade in" role="alert"> <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button> <strong>Thank you for your feedback !</strong> If your message was pertinent we will recontact you.. Maybe... If we got the time. </div>');
			event.preventDefault();
		});
	});

</script>