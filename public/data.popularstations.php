<?php
    require_once '../common/common.php';
	
	// Returns full name of the carrier if known.
	function get_carrier_name($callsign) {
		global $db;
		
		$sql = "SELECT `name` FROM `carrier_names` WHERE `callsign` = :callsign";
		$stmt = $db->prepare($sql);
		$stmt->bindParam(":callsign", $callsign, PDO::PARAM_STR);
		$stmt->execute();
		
		$name = $stmt->fetchColumn();
		if ($name === false) {
			return $callsign;
		} else {
			return $name . " " . $callsign;
		}
	}
    
    $db = create_database();
	
	$startTime = time() - (60 * 60 * 24);
	$sql = "
		SELECT 
			`docked_messages`.`system_id`,
			`docked_messages`.`market_id`,
			`docked_messages`.`timestamp`,
			`systems`.`name` AS `system_name`,
			`markets`.`name` AS `market_name`,
			`markets`.`market_type`,
			COUNT(*) AS `count`
		FROM `docked_messages`, `systems`, `markets`
		WHERE `docked_messages`.`timestamp` >= :startTime
		  AND `docked_messages`.`system_id` = `systems`.`id`
		  AND `docked_messages`.`market_id` = `markets`.`id`
		GROUP BY `market_id` 
		ORDER BY `count` DESC
		LIMIT 50
	";
	$markets = $db->prepare($sql);
	$markets->bindParam(":startTime", $startTime, PDO::PARAM_INT);
	$markets->execute();
    
    $smarty = create_smarty();
	$smarty->assign('markets', $markets);
    $smarty->display('data.popularstations.tpl');