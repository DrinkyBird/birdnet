<?php
    require_once 'common.php';
    require_once 'libs/Smarty.class.php';
	
	$now = time();
    
    $tableName = "updates";
    
    $dsn = "mysql:host=".DB_HOST.";dbname=".DB_NAME.";charset=utf8mb4";
    $db = new PDO($dsn, DB_USERNAME, DB_PASSWORD, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_OBJ,
        PDO::ATTR_EMULATE_PREPARES   => false,
    ]);
    
    $archives = [];
    $sql = "SELECT `version`, `date` FROM $tableName ORDER BY `date` DESC";
    $stmt = $db->query($sql);
	$archives = [];
	foreach ($stmt as $row) {
		$archives[$row->version] = $row->date;
	}
    
    $where_clause = "";
    
    $filter_version = filter_input(INPUT_GET, 'version', FILTER_DEFAULT, [
        'options' => [
            'default' => null,
        ]
    ]);
    $filter_notes = filter_input(INPUT_GET, 'notes', FILTER_DEFAULT, [
        'options' => [
            'default' => null,
        ]
    ]);
    
    add_filter_clause($filter_notes, '`notes` LIKE CONCAT("%", :notes, "%")');
    add_filter_clause($filter_version, '`version`=:version');
    
    function add_filter_param($stmt, $name, $value, $type) {
        if ($value === null) {
            return;
        }
        
        $stmt->bindParam($name, $value, $type);
    }
    
    function add_filter_params($stmt) {
        global $filter_version, $filter_notes;
        add_filter_param($stmt, ':version', $filter_version, PDO::PARAM_STR);
        add_filter_param($stmt, ':notes', $filter_notes, PDO::PARAM_STR);
    }
    
    function add_filter_clause($value, $clause) {
        if ($value === null) {
            return;
        }
        
        global $where_clause;
        
        if (strlen($where_clause) == 0) {
            $where_clause = 'WHERE ' . $clause;
        } else {
            $where_clause .= ' AND ' . $clause;
        }
    }
    
    $sql = "SELECT COUNT(*) FROM $tableName $where_clause";
    $stmt = $db->prepare($sql);
    add_filter_params($stmt);
    $stmt->execute();
    $total = $stmt->fetchColumn();
    
    $limit = 10;
    
    $pages = ceil($total / $limit);
    
    $page = min($pages, filter_input(INPUT_GET, 'page', FILTER_VALIDATE_INT, [ 
        'options' => [
            'default' => 1,
            'min_range' => 1
        ]
    ]));
    
    $offset = ($page - 1) * $limit;
    $start = $offset + 1;
    $end = min($offset + $limit, $total);
    
    if ($total > 0) {
		$sql = "SELECT * FROM $tableName $where_clause ORDER BY date DESC LIMIT $limit OFFSET $offset";
		$stmt = $db->prepare($sql);
		add_filter_params($stmt);
		$stmt->execute();
		$rows = $stmt->fetchAll();
	} else {
		$rows = [];
	}
    
    function format_timestamp($ts) {
        $f = date('d M Y', $ts);
        $parts = explode(" ", $f);
        $year = intval($parts[2]) + 1286;
        return $parts[0] . " " . $parts[1] . " " . $year;
    }
    
    $filter_url = '';
    function filterurl_add($key, $value) {
        global $filter_url;
        if ($value === null || empty($value)) {
            return;
        }
        $filter_url .= "&$key=". urlencode($value);
    }
    filterurl_add("version", $filter_version);
    filterurl_add("notes", $filter_notes);
    
    function get_image($row) {
        if ($row->image == null) {
            return null;
        }
        
        $s = explode(",", $row->image);
        return $s[0];
    }
	
	function highlight_search($text, $search) {
		global $filter_text;
		if ($search === null || empty($search)) {
			return $text;
		}
		return preg_replace("/$search/i", '<span class="highlight">$0</span>', $text);
	}
    
    $pageTitle = (isset($_GET['version'])) ? $rows[0]->title . " &mdash; ": "";
	$isSingleArticle = ($filter_version !== null);
    
    $smarty = new Smarty();
    $smarty->setTemplateDir('tpl');
    $smarty->assign('pageTitle', $pageTitle);
    $smarty->assign('filter_version', $filter_version);
    $smarty->assign('filter_notes', $filter_notes);
    $smarty->assign('stmt', $stmt);
    $smarty->assign('archives', $archives);
    $smarty->assign('rows', $rows);
    $smarty->assign('page', $page);
    $smarty->assign('pages', $pages);
    $smarty->assign('is_single_article', $isSingleArticle);
    $smarty->display('updates.tpl');
