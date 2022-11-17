<?php
    require_once '../common/common.php';
    
    $db = create_database();
    
    $statuses = $db->query("SELECT * FROM `status`  ORDER BY `timestamp` DESC");
    
    $smarty = create_smarty();
    $smarty->assign('statuses', $statuses);
    $smarty->assign('attributes', $attributes);
    $smarty->display('status.tpl');
?>