<h2>List of news</h2>
<ul>
	<li>
		<a href="/article/1/">XSS ?</a>
	</li>
	<li>
		<a href="/article/2/">Rewriting URL with Apache</a>
	</li>
	<li>
		<a href="/article/3/">SQLi, how to protect ?</a>
	</li>
</ul>

<?php
	if(isset($_GET['id']) && $_GET['id'] == 1) {
?>

<div class="box">
	<h3>The XSS</h3>
	<p>XSS are one of the more common vulnerability outhere.</p>
	<p>It is a type of computer security vulnerability typically found in web applications. XSS enables attackers to inject client-side scripts into web pages viewed by other users. A cross-site scripting vulnerability may be used by attackers to bypass access controls such as the same-origin policy.</p>
	<p>To prevent against XSS, <a href="/">UltraSecure</a> use a PHP function : <a href="http://php.net/manual/en/function.htmlentities.php">htmlentities</a>. You really should do the same. PHP is awesome !</p>
</div>

<?php
	}else if(isset($_GET['id']) && $_GET['id'] == 2){
?>

<div class="box">
	<h3>Rewriting URL with Apache</h3>
	<p>Apache's <a href="https://httpd.apache.org/docs/current/mod/mod_rewrite.html">mod_rewrite</a> is really usefull.</p>
	<p>With just a few lines in an Apache config you can get beautiful URLs. Here is an example based on the <a href="/">UltraSecure</a>'s website :</p>
	<pre>RewriteRule ^([a-z0-9%_\.]+)/$ index.php?p=$1 [NC,L]</pre>
	<hr>
	<p>So for example a request asking for : <pre>/home/</pre> would be transform into <pre>/index.php?p=home</pre>Awesome right ? ;)</p>
</div>

<?php
	}else if(isset($_GET['id']) && $_GET['id'] == 3){
?>

<div class="box">
	<h3>SQLi</h3>
	<p>Once again, a big and old threat !</p>
	<p>SQL injection is a code injection technique, used to attack data-driven applications, in which malicious SQL statements are inserted into an entry field for execution (e.g. to dump the database contents to the attacker).</p>
	<p>For example, here is a vulnerable code :</p>
	<pre>statement = <pre style="display: inline;">"SELECT * FROM users WHERE name = '</pre>" + userName + "<pre style="display: inline;">';</pre>"</pre>
	<p>To prevent against SQLi, <a href="/">UltraSecure</a> use a MySQL prepared statements : <a href="http://php.net/manual/en/mysqli.quickstart.prepared-statements.php"><b>prepare</b> function from PHP</a>. Have an happy coding :)</p>
</div>

<?php
	}
?>