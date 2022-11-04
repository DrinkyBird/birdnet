<?php
    require_once '../common/common.php';
    
    function get_image($row) {
        if ($row->image == null) {
            return null;
        }
        
        $s = explode(",", $row->image);
        return $s[0];
    }
    
    $db = create_database();
    
    $sql = "SELECT * FROM `updates` ORDER BY `date` DESC LIMIT 10";
    $stmt = $db->query($sql);
    
    header("Content-Type: text/xml");
    $smarty = create_smarty();
    $smarty->assign('rows', $stmt);
    $smarty->display('updates.rss.tpl');
