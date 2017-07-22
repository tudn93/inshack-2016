<?php

require_once 'Twig/Autoloader.php';

Twig_Autoloader::register();

$loader = new Twig_Loader_Filesystem('templates');
$twig = new Twig_Environment($loader, array(
    'cache' => '.cache',
));

echo $twig->render('index.html', array('name' => 'Fabien'));
/*
	index normal avec un lien vers /admin (transformer votre code html en pdf)
	service HTML to PDF
	injection de template x)

	wkhtmltopdf + twig

	XSS dans le bot wkhtmltopdf => leak cookie (alert or document write)
	permet d'accèder à l'admin
	/admin/1234.html
	depuis l'admin modif du code de template twig
*/
