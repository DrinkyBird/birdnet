<?php
    require_once 'common.php';
    require_once 'libs/Smarty.class.php';
    
    $dsn = "mysql:host=".DB_HOST.";dbname=".DB_NAME.";charset=utf8mb4";
    $db = new PDO($dsn, DB_USERNAME, DB_PASSWORD, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_OBJ,
        PDO::ATTR_EMULATE_PREPARES   => false,
    ]);
    
    $id = $_GET["id"];
	
	$attributes = [];
	
    $sql = "SELECT * FROM `store` WHERE `sku`=:id";
    $stmt = $db->prepare($sql);
    $stmt->bindParam(":id", $id, PDO::PARAM_INT);
    $stmt->execute();
    $item = $stmt->fetch();
	
	if ($item !== false) {
		$sql = "SELECT `attribute` FROM `store_attributes` WHERE `sku` = :id";
		$stmt = $db->prepare($sql);
		$stmt->bindParam(":id", $item->sku, PDO::PARAM_STR);
		$stmt->execute();
		foreach ($stmt as $row) {
			$attributes[] = $row->attribute;
		}
	}
	
	$doc = new DomDocument();
	$doc->loadHTML($item->short_description);
	$description = $doc->documentElement->childNodes[0]->childNodes[0]->nodeValue;
    
    $smarty = new Smarty();
    $smarty->setTemplateDir('tpl');
    $smarty->assign('item', $item);
    $smarty->assign('attributes', $attributes);
    $smarty->assign('description', $description);
    $smarty->display('store.item.tpl');
?>