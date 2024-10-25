<?php
    require_once '../common/common.php';
    require_once '../common/store.php';

    $db = create_database();

    $used_attrs = [];

    $sql = "SELECT `attribute` FROM `store_attributes` GROUP BY `attribute`";
    $stmt = $db->query($sql);
    foreach ($stmt as $row) {
        $used_attrs[] = $row->attribute;
    }

    $known_attrs = [];
    foreach (STORE_ATTRIBUTES as $key => $_) {
        $known_attrs[] = $key;
    }

    $diff = array_diff($used_attrs, $known_attrs);

    foreach ($diff as $attr) {
        echo "Unknown attribute $attr used by:\n";
        $sql = "SELECT `sku`, `title` FROM `store` WHERE `sku` IN (SELECT `sku` FROM `store_attributes` WHERE `attribute` = :attr GROUP BY `sku`)";
        $stmt = $db->prepare($sql);
        $stmt->bindParam(":attr", $attr);
        $stmt->execute();

        foreach ($stmt as $row) {
            echo "\t" . $row->sku . " - " . $row->title . "\n";
        }

        echo "\n";
    }
