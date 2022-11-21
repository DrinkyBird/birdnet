<?php
    require_once '../common/common.php';
    require_once '../common/store.php';

    $filter_attributes = [];
    if (isset($_GET["attribute"]) && is_array($_GET["attribute"])) {
        foreach ($_GET["attribute"] as $attr) {
            if (is_numeric($attr)) {
                $filter_attributes[] = intval($attr);
            }
        }
    }

    $filter_available = "";
    if (isset($_GET["available"])) {
        $filter_available = $_GET["available"];
    }

    $filter_discounted = "";
    if (isset($_GET["discounted"])) {
        $filter_discounted = $_GET["discounted"];
    }

    $smarty = create_smarty();
    $smarty->assign("filter_attributes", $filter_attributes);
    $smarty->assign("filter_available", $filter_available);
    $smarty->assign("filter_discounted", $filter_discounted);
    $smarty->assign("STORE_ATTRIBUTES", STORE_ATTRIBUTES);
    $smarty->display("store.filter.tpl");