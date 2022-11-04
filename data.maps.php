<?php
    require_once 'common.php';
    require_once 'libs/Smarty.class.php';
	
	function get_timing($path) {
		return intval(file_get_contents("maps/" . $path . ".time"));
	}
    
    $smarty = new Smarty();
    $smarty->setTemplateDir('tpl');
    $smarty->display('data.maps.tpl');