<?php
    require_once '../common/common.php';
    
    $db = create_database();
	
	$filter_name = null;
	if (isset($_GET["name"])) {
		$filter_name = $_GET["name"];
	}
	
	$filter_attributes = [];
	if (isset($_GET["attribute"])) {
		if (is_array($_GET["attribute"])) {
			$filter_attributes = $_GET["attribute"];
		} else {
			$filter_attributes = [ $_GET["attribute"] ];
		}
	}		
    
	$wherestr = "";
	if ($filter_name !== null) { $wherestr .= " AND `title` LIKE CONCAT('%', :title, '%')"; }
	
    $sql = "
		SELECT 
			*,
			(`current_price` < `original_price`) AS `discounted`
		FROM `store` 
		WHERE 1 $wherestr
		ORDER BY discounted DESC, `first_seen` DESC
	";
	
    $items = $db->prepare($sql);
	$items->bindParam(":title", $filter_name, PDO::PARAM_STR);
    $items->execute();
	
	$itemCount = 0;
	if ($items === false) {
		$items = [];
	} else {
		$itemCount = $items->rowCount();
	}
	
	$sql = "SELECT `attribute` FROM `store_attributes` GROUP BY `attribute` ORDER BY `attribute` ASC";
	$stmt = $db->query($sql);
	$attributes = [];
	foreach ($stmt as $row) {
		$attributes[] = $row->attribute;
	}
	
    $smarty = create_smarty();
    $smarty->assign('items', $items);
    $smarty->assign('itemCount', $itemCount);
    $smarty->assign('attributes', $attributes);
    $smarty->display('store.tpl');
?>