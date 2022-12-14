<?php
    require_once '../common/common.php';
    require_once '../common/store.php';
    
    $db = create_database();
    
    $filter_name = null;
    if (isset($_GET["name"]) && !empty($_GET["name"])) {
        $filter_name = $_GET["name"];
    }

    $filter_available = null;
    if (isset($_GET["available"])) {
        if ($_GET["available"] === "true") {
            $filter_available = true;
        } else if ($_GET["available"] === "false") {
            $filter_available = false;
        }
    }

    $filter_discounted = null;
    if (isset($_GET["discounted"])) {
        if ($_GET["discounted"] === "true") {
            $filter_discounted = true;
        } else if ($_GET["discounted"] === "false") {
            $filter_discounted = false;
        }
    }
    
    $filter_attributes = [];
    if (isset($_GET["attribute"])) {
        if (is_array($_GET["attribute"])) {
            foreach ($_GET["attribute"] as $attr) {
                if (is_numeric($attr)) {
                    $filter_attributes[] = intval($attr);
                }
            }
        } else {
            $filter_attributes = [ $_GET["attribute"] ];
        }
    }

    $filter_client_version = null;
    if (isset($_GET["client_version"]) && is_numeric($_GET["client_version"])) {
        $filter_client_version = intval($_GET["client_version"]);
    }

    $filter_season = null;
    if (isset($_GET["season"]) && is_numeric($_GET["season"])) {
        $filter_season = intval($_GET["season"]);
    }
    
    $wherestr = "";
    if ($filter_name !== null) {
        $wherestr .= " AND `title` LIKE CONCAT('%', :title, '%')";
    }

    if ($filter_available !== null) {
        $wherestr .= " AND `available` = :available";
    }

    if ($filter_discounted !== null) {
        $wherestr .= " AND (`current_price` < `original_price`) = :discounted";
    }

    if ($filter_client_version !== null) {
        $wherestr .= " AND `minimum_client_version` >= :client_version";
    }

    if ($filter_season !== null) {
        $wherestr .= " AND `minimum_season` >= :season";
    }

    $attr_params = [];
    if (!empty($filter_attributes)) {
        for ($i = 0; $i < count($filter_attributes); $i++) {
            $attr_params[] = ":attr_" . $i;
        }
        $attr_tuple_str = implode(",", $attr_params);
        $attr_count = count($filter_attributes);

        $wherestr .= " 
            AND `sku` IN (
                SELECT `sku`
                FROM `store_attributes`
                WHERE `attribute` IN ($attr_tuple_str)
                GROUP BY `sku`
                HAVING COUNT(*) = $attr_count
            )
        ";
    }
    
    $sql = "
        SELECT 
            *,
            (`current_price` < `original_price` AND `available`) AS `discounted`
        FROM `store` 
        WHERE 1 $wherestr
        ORDER BY `discounted` DESC, `first_seen` DESC
    ";

    $items = $db->prepare($sql);
    if ($filter_name !== null) {
        $items->bindParam(":title", $filter_name, PDO::PARAM_STR);
    }
    if ($filter_available !== null) {
        $items->bindParam(":available", $filter_available);
    }
    if ($filter_discounted !== null) {
        $items->bindParam(":discounted", $filter_discounted);
    }
    if ($filter_client_version !== null) {
        $items->bindParam(":client_version", $filter_client_version);
    }
    if ($filter_season !== null) {
        $items->bindParam(":season", $filter_season);
    }
    for ($i = 0; $i < count($filter_attributes); $i++) {
        $items->bindParam($attr_params[$i], $filter_attributes[$i]);
    }
    $items->execute();
    
    $itemCount = 0;
    if ($items === false) {
        $items = [];
    } else {
        $itemCount = $items->rowCount();
    }
    
    $smarty = create_smarty();
    $smarty->assign('items', $items);
    $smarty->assign('itemCount', $itemCount);
    $smarty->assign('filter_name', $filter_name);
    $smarty->assign('filter_available', $filter_available);
    $smarty->assign('filter_discounted', $filter_discounted);
    $smarty->assign('filter_client_version', $filter_client_version);
    $smarty->assign('filter_season', $filter_season);
    $smarty->assign('filter_attributes', $filter_attributes);
    $smarty->display('store.tpl');
?>