<?php
    require_once '../common/common.php';
    
    $db = create_database();
    
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
    
    $smarty = create_smarty();
    $smarty->setTemplateDir('tpl');
    $smarty->assign('goal', $goal);
    $smarty->assign('sheetId', $sheetId);
    $smarty->display('goalgraph.tpl');
?>