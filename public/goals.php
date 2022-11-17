<?php
    require_once '../common/common.php';
    
    $db = create_database();
    
    $now = time();
    
    $language = get_user_language();
    $table = "goals_" . $language;
    
    $sql = "SELECT * FROM $table WHERE expiry>:now ORDER BY expiry DESC";
    $stmt = $db->prepare($sql);
    $stmt->bindParam(":now", $now, PDO::PARAM_INT);
    $stmt->execute();
    $active = $stmt->fetchAll();
    
    $sql = "SELECT * FROM $table WHERE expiry<:now ORDER BY expiry DESC";
    $stmt = $db->prepare($sql);
    $stmt->bindParam(":now", $now, PDO::PARAM_INT);
    $stmt->execute();
    $expired = $stmt->fetchAll();
    
    $smarty = create_smarty();
    $smarty->assign('active', $active);
    $smarty->assign('expired', $expired);
    $smarty->assign('language', $language);
    $smarty->display('goals.tpl');
?>