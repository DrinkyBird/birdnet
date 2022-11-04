<?php
    require_once 'common.php';
    require_once 'libs/Smarty.class.php';
    
    $dsn = "mysql:host=".DB_HOST.";dbname=".DB_NAME.";charset=utf8mb4";
    $db = new PDO($dsn, DB_USERNAME, DB_PASSWORD, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_OBJ,
        PDO::ATTR_EMULATE_PREPARES   => false,
    ]);
    
    $id = filter_input(INPUT_GET, 'id', FILTER_VALIDATE_INT, [
        'options' => [
            'default' => null,
        ]
    ]);
    
    $table = "goals_" . get_user_language();
    
    $sql = "SELECT * FROM $table WHERE id=:id";
    $stmt = $db->prepare($sql);
    $stmt->bindParam(":id", $id, PDO::PARAM_INT);
    $stmt->execute();
    $goal = $stmt->fetch();
	
	$sql = "SELECT * FROM `goals_sheets` WHERE `goal_id` = :id";
	$stmt = $db->prepare($sql);
    $stmt->bindParam(":id", $id, PDO::PARAM_INT);
    $stmt->execute();
    $res = $stmt->fetch();
	$sheetId = null;
	if ($res !== false) {
		$sheetId = $res->sheet_id;
	}
    
    $smarty = new Smarty();
    $smarty->setTemplateDir('tpl');
    $smarty->assign('goal', $goal);
    $smarty->assign('sheetId', $sheetId);
    $smarty->display('goalgraph.tpl');
?>