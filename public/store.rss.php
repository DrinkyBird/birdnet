<?php
    require_once '../common/common.php';
    
    $db = create_database();
    
    $sql = "
		SELECT * FROM `store` ORDER BY `first_seen` DESC LIMIT 125
	";
    $stmt = $db->prepare($sql);
    $stmt->execute();
	
	header("Content-Type: text/xml");
    $smarty = create_smarty();
    $smarty->assign('rows', $stmt);
    $smarty->display('store.rss.tpl');
?>
