<?php
    require_once 'common.php';
    require_once 'libs/Smarty.class.php';
    
    function get_image($row) {
        if ($row->image == null) {
            return null;
        }
        
        $s = explode(",", $row->image);
        return $s[0];
    }
    
    $dsn = "mysql:host=".DB_HOST.";dbname=".DB_NAME.";charset=utf8mb4";
    $db = new PDO($dsn, DB_USERNAME, DB_PASSWORD, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_OBJ,
        PDO::ATTR_EMULATE_PREPARES   => false,
    ]);
    
    $sql = "SELECT * FROM `updates` ORDER BY `date` DESC LIMIT 10";
    $stmt = $db->query($sql);
    
    header("Content-Type: text/xml");
    $smarty = new Smarty();
    $smarty->setTemplateDir('tpl');
    $smarty->assign('rows', $stmt);
    $smarty->display('updates.rss.tpl');
