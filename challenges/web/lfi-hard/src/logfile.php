<p>
	Bellow is your log file from this server, don't be afraid we don't keep these infos. But be aware that every website you visit see this !
</p>
<p>
	<small>
		Note : you can access your log file <a href="/<?php echo $LOGS_DIR . $log_file ?>">directy from here</a>.
	</small>
</p>
<pre><?php	echo htmlentities(file_get_contents($LOGS_DIR . $log_file)); ?></pre>