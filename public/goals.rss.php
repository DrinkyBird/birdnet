<?php
    require_once '../common/common.php';
    
    $db = create_database();
    
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
    $smarty = create_smarty();
    $smarty->assign('active', $stmt);
    $smarty->assign('language', $lang);
    $smarty->display('goals.rss.tpl');
?>