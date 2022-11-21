<?php
    require_once '../common/common.php';
    require_once '../common/store.php';
    
    $db = create_database();
    
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
    
    $smarty = create_smarty();
    $smarty->assign('item', $item);
    $smarty->assign('attributes', $attributes);
    $smarty->assign('description', $description);
    $smarty->display('store.item.tpl');
?>