<?php
    require_once 'common.php';
    require_once 'libs/Smarty.class.php';
    
    $dsn = "mysql:host=".DB_HOST.";dbname=".DB_NAME.";charset=utf8mb4";
    $db = new PDO($dsn, DB_USERNAME, DB_PASSWORD, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_OBJ,
        PDO::ATTR_EMULATE_PREPARES   => false,
    ]);
    
    $now = time();
    
	$lang = "en";
	if (isset($_GET["lang"]) && in_array($_GET["lang"], LANGUAGES, true)) {
		$lang = $_GET["lang"];
	}
    
    $table = "goals_" . $lang;
    
    $sql = "SELECT * FROM $table WHERE expiry > :now ORDER BY expiry DESC";
    $stmt = $db->prepare($sql);
    $stmt->bindParam(":now", $now, PDO::PARAM_INT);
    $stmt->execute();
	
	header("Content-Type: text/xml");
    $smarty = new Smarty();
    $smarty->setTemplateDir('tpl');
    $smarty->assign('active', $stmt);
    $smarty->assign('language', $lang);
    $smarty->display('goals.rss.tpl');
?>