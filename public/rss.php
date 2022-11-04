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
	
	$lang = "en";
	if (isset($_GET["lang"]) && in_array($_GET["lang"], LANGUAGES, true)) {
		$lang = $_GET["lang"];
	}
    $sql = "SELECT * FROM posts_".$lang." ORDER BY date DESC LIMIT 10";
    $stmt = $db->query($sql);
    
	header("Content-Type: text/xml");
    $smarty = create_smarty();
    $smarty->assign('language', $lang);
    $smarty->assign('rows', $stmt);
    $smarty->display('rss.tpl');
?>