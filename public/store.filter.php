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

    $filter_client_version = "";
    if (isset($_GET["client_version"]) && is_numeric($_GET["client_version"])) {
        $filter_client_version = intval($_GET["client_version"]);
    }

    $filter_season = "";
    if (isset($_GET["season"]) && is_numeric($_GET["season"])) {
        $filter_season = intval($_GET["season"]);
    }

    $smarty = create_smarty();
    $smarty->assign("filter_attributes", $filter_attributes);
    $smarty->assign("filter_available", $filter_available);
    $smarty->assign("filter_discounted", $filter_discounted);
    $smarty->assign("filter_client_version", $filter_client_version);
    $smarty->assign("filter_season", $filter_season);
    $smarty->display("store.filter.tpl");