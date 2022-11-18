<?php
    require_once '../common/common.php';
    
    $now = time();
    
    $language = get_user_language();
    $tableName = "posts_" . $language;
    
    $db = create_database();
    
    $archives = [];
    $sql = "SELECT date FROM $tableName";
    $stmt = $db->query($sql);
    foreach ($stmt as $row) {
        $str = date('F Y', $row->date);
        $exp = explode(" ", $str);
        $str = $exp[0] . " " . (intval($exp[1]) + 1286);
        if (array_key_exists($str, $archives)) {
            $data = $archives[$str];
            $data[0] = min($row->date, $data[0]);
            $data[1] = max($row->date, $data[1]);
            $archives[$str] = $data;
        } else {
            $archives[$str] = [$row->date, $row->date];
        }
    }
    
    function archives_sort($a, $b) {
        return $a[0] < $b[0];
    }
    uasort($archives, "archives_sort");
	
	function parse_date($in, $def) {
		if (is_numeric($in)) {
			return intval($in);
		}
		
		$parsed = strtotime($in);
		if ($parsed !== false) {
			return $parsed;
		}
		
		return $def;
	}
    
    $where_clause = "";
    
    $filter_title = filter_input(INPUT_GET, 'title', FILTER_DEFAULT, [
        'options' => [
            'default' => null,
        ]
    ]);
    $filter_text = filter_input(INPUT_GET, 'text', FILTER_DEFAULT, [
        'options' => [
            'default' => null,
        ]
    ]);
    $filter_guid = filter_input(INPUT_GET, 'guid', FILTER_DEFAULT, [
        'options' => [
            'default' => null,
        ]
    ]);
    
    $filter_from = isset($_GET['from']) ? parse_date($_GET['from'], 0) : 0;
    $filter_to = isset($_GET['to']) ? parse_date($_GET['to'], $now) : $now;
    $html_from = isset($_GET['from']) ? date('Y-m-d', $filter_from) : '';
    $html_to = isset($_GET['to']) ? date('Y-m-d', $filter_to) : '';
    $extracts_only = isset($_GET['extractsonly']);
    
    add_filter_clause($filter_title, 'title LIKE CONCAT("%", :title, "%")');
    add_filter_clause($filter_text, 'text LIKE CONCAT("%", :text, "%")');
    add_filter_clause($filter_guid, 'guid=:guid');
    add_filter_clause($filter_from, 'date >= :from');
    add_filter_clause($filter_to, 'date <= :to');
    
    function add_filter_param($stmt, $name, $value, $type) {
        if ($value === null) {
            return;
        }
        
        $stmt->bindParam($name, $value, $type);
    }
    
    function add_filter_params($stmt) {
        global $filter_title, $filter_text, $filter_guid, $filter_from, $filter_to;
        add_filter_param($stmt, ':title', $filter_title, PDO::PARAM_STR);
        add_filter_param($stmt, ':text', $filter_text, PDO::PARAM_STR);
        add_filter_param($stmt, ':guid', $filter_guid, PDO::PARAM_STR);
        add_filter_param($stmt, ':from', $filter_from, PDO::PARAM_INT);
        add_filter_param($stmt, ':to', $filter_to, PDO::PARAM_INT);
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
    filterurl_add("title", $filter_title);
    filterurl_add("text", $filter_text);
    filterurl_add("guid", $filter_guid);
    if ($filter_from != 0) { filterurl_add("from", $filter_from); }
    if ($filter_to != $now) { filterurl_add("to", $filter_to); }
    if ($extracts_only) { $filter_url .= "&extractsonly"; }
    
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
    
    $pageTitle = (isset($_GET['guid'])) ? $rows[0]->title . " &mdash; ": "";
    $isSingleArticle = ($filter_guid !== null);
    
    $smarty = create_smarty();
    $smarty->assign('pageTitle', $pageTitle);
    $smarty->assign('filter_title', $filter_title);
    $smarty->assign('filter_text', $filter_text);
    $smarty->assign('filter_url', $filter_url);
    $smarty->assign('filter_from', $html_from);
    $smarty->assign('filter_to', $html_to);
    $smarty->assign('stmt', $stmt);
    $smarty->assign('archives', $archives);
    $smarty->assign('rows', $rows);
    $smarty->assign('page', $page);
    $smarty->assign('pages', $pages);
    $smarty->assign('is_single_article', $isSingleArticle);
    $smarty->assign('language', $language);
    $smarty->assign('extracts_only', $extracts_only);
    $smarty->display('news.tpl');
