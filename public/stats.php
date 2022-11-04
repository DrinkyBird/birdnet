<?php
    require_once '../common/common.php';
    
    $db = create_database();
    
    $sql = 'SELECT SUM(ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024), 2)) AS "SIZE IN MB" FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = "' . DB_NAME . '"';
    $stmt = $db->query($sql);
    $usage = $stmt->fetchColumn();
    
    $sql = 'SELECT COUNT(id) FROM `systems`';
    $stmt = $db->query($sql);
    $systemCount = $stmt->fetchColumn();
    
    $sql = 'SELECT COUNT(body_id) FROM `bodies`';
    $stmt = $db->query($sql);
    $bodyCount = $stmt->fetchColumn();
    
    $sql = 'SELECT COUNT(id) FROM `markets`';
    $stmt = $db->query($sql);
    $marketCount = $stmt->fetchColumn();
    
    $sql = 'SELECT COUNT(id) FROM `eddn`';
    $stmt = $db->query($sql);
    $eddnMessageCount = $stmt->fetchColumn();
    
    $newsCounts = [];
    $goalCounts = [];
    
    foreach (LANGUAGES as $language) {
        $table = "posts_" . $language;
        $sql = "SELECT COUNT(*) FROM `$table`";
        $stmt = $db->query($sql);
        $newsCounts[$language] = $stmt->fetchColumn();
        
        $table = "goals_" . $language;
        $sql = "SELECT COUNT(*) FROM `$table`";
        $stmt = $db->query($sql);
        $goalCounts[$language] = $stmt->fetchColumn();
    }
    
    $smarty = create_smarty();
    $smarty->assign('usage', $usage);
    $smarty->assign('systemCount', $systemCount);
    $smarty->assign('bodyCount', $bodyCount);
    $smarty->assign('marketCount', $marketCount);
    $smarty->assign('newsCounts', $newsCounts);
    $smarty->assign('goalCounts', $goalCounts);
    $smarty->assign('eddnMessageCount', $eddnMessageCount);
    $smarty->display('stats.tpl');