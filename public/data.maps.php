<?php
    require_once '../common/common.php';
	
	function get_timing($path) {
		return intval(file_get_contents("maps/" . $path . ".time"));
	}
    
    $smarty = create_smarty();
    $smarty->display('data.maps.tpl');