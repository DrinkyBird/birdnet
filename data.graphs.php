<?php
    require_once 'common.php';
    require_once 'libs/Smarty.class.php';
	
    $smarty = new Smarty();
    $smarty->setTemplateDir('tpl');
    $smarty->display('data.graphs.tpl');