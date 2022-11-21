<?php
    require_once '../config.php';
    require_once '../lib/smarty/libs/Smarty.class.php';

    const LANGUAGES = ['en', 'es', 'de', 'fr', 'ru'];
    const LANGUAGE_NAMES = ['English', 'español', 'Deutsche', 'français', 'русский'];
    
    function create_smarty() {
        $appRoot = dirname(dirname(__FILE__));
       
        $smarty = new \Smarty();
        $smarty->setTemplateDir($appRoot . '/templates');
        $smarty->setCompileDir($appRoot . '/runtime/templates_c');
        $smarty->setCacheDir($appRoot . '/runtime/cache');
        
        return $smarty;
    }
    
    function create_database() {
        $dsn = "mysql:host=".DB_HOST.";dbname=".DB_NAME.";charset=utf8mb4";
        $db = new PDO($dsn, DB_USERNAME, DB_PASSWORD, [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_OBJ,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ]);
        
        return $db;
    }
    
    if (!function_exists('str_ends_with')) {
        function str_ends_with( $haystack, $needle ) {
            $length = strlen( $needle );
            if( !$length ) {
                return true;
            }
            return substr( $haystack, -$length ) === $needle;
        }
    }
    
    // Format the text of a Galnet article
    function format_text($text) {
        $text = str_replace("\r", '', $text);
        $paragraphs = '';

        foreach (explode("\n", $text) as $line) {
            if (trim($line)) {
                $paragraphs .= '<p>' . htmlspecialchars($line, ENT_HTML5) . '</p>';
            }
        }

        return $paragraphs;
    }
    
    // Generate an extract from the text of a Galnet article
    function generate_extract($text) {
        $text = str_replace("\r", "", $text);
        $lines = explode("\n", $text);
        
        foreach ($lines as $line) {
            if (empty($line)) continue;
            
            if (strpos($line, " Federation ALERT") !== false) {
                continue;
            }
            
            $sentences = explode(". ", $line);
            $sentence = $sentences[0];
            if (!str_ends_with($sentence, ".")) {
                $sentence .= ".";
            }
            
            return $sentence;
        }
        
        return "???";
    }
    
    function get_default_language() {
        if (isset($_SERVER['HTTP_ACCEPT_LANGUAGE']) && strlen($_SERVER['HTTP_ACCEPT_LANGUAGE']) >= 2) {
            $lang = substr($_SERVER['HTTP_ACCEPT_LANGUAGE'], 0, 2);
            if (in_array($lang, LANGUAGES, true)) {
                return $lang;
            }
        }
        return 'en';
    }
    
    function get_user_language() {
        if (isset($_GET['lang']) && in_array($_GET['lang'], LANGUAGES, true)) {
            return $_GET['lang'];
        } else if (!isset($_COOKIE['birdnet_language']) || !in_array($_COOKIE['birdnet_language'], LANGUAGES, true)) {
            $default = get_default_language();
            setcookie('birdnet_language', $default);
            return $default;
        } else {
            return $_COOKIE['birdnet_language'];
        }
    }
    
    function smarty_modifier_birdescape($string) {
        return htmlspecialchars($string, ENT_HTML5);
    }

    const ECONOMY_NAMES = [
        '$economy_Agri;' => "Agriculture",
        '$economy_Colony;' => "Colony",
        '$economy_Extraction;' => "Extraction",
        '$economy_HighTech;' => "High Tech",
        '$economy_Industrial;' => "Industrial",
        '$economy_Military;' => "Military",
        '$economy_None;' => "None",
        '$economy_Refinery;' => "Refinery",
        '$economy_Service;' => "Service",
        '$economy_Terraforming;' => "Terraforming",
        '$economy_Tourism;' => "Tourism",
        '$economy_Prison;' => "Prison",
        '$economy_Damaged;' => "Damaged",
        '$economy_Rescue;' => "Rescue",
        '$economy_Repair;' => "Repair",
        '$economy_Carrier;' => "Private Enterprise"
    ];
    
    function get_economy_name($key) {
        if (array_key_exists($key, ECONOMY_NAMES)) {
            return ECONOMY_NAMES[$key];
        } else {
            return $key;
        }
    }

    const GOVERNMENT_NAMES = [
        '$government_Anarchy;' => 'Anarchy',
        '$government_Communism;' => 'Communism',
        '$government_Confederacy;' => 'Confederacy',
        '$government_Cooperative;' => 'Cooperative',
        '$government_Corporate;' => 'Corporate',
        '$government_Democracy;' => 'Democracy',
        '$government_Dictatorship;' => 'Dictatorship',
        '$government_Feudal;' => 'Feudal',
        '$government_Imperial;' => 'Imperial',
        '$government_None;' => 'None',
        '$government_Patronage;' => 'Patronage',
        '$government_PrisonColony;' => 'Prison Colony',
        '$government_Prison;' => 'Prison',
        '$government_Theocracy;' => 'Theocracy',
        '$government_Engineer;' => 'Engineer',
        '$government_Carrier;' => 'Private Ownership'
    ];
    
    function get_government_name($key) {
        if (array_key_exists($key, GOVERNMENT_NAMES)) {
            return GOVERNMENT_NAMES[$key];
        } else {
            return $key;
        }
    }

    const SECURITY_NAMES = [
        '$GAlAXY_MAP_INFO_state_anarchy;' => 'Anarchy',
        '$GALAXY_MAP_INFO_state_lawless;' => 'Lawless',
        '$SYSTEM_SECURITY_high;' => 'High',
        '$SYSTEM_SECURITY_low;' => 'Low',
        '$SYSTEM_SECURITY_medium;' => 'Medium'
    ];
    
    function get_security_name($key) {
        if (array_key_exists($key, SECURITY_NAMES)) {
            return SECURITY_NAMES[$key];
        } else {
            return $key;
        }
    }

    const POWERPLAY_IDS = [
        'Edmund Mahon' => 'mahon',

        'Aisling Duval' => 'duval',
        'A. Lavigny-Duval' => 'lavignyduval',
        'Denton Patreus' => 'patreus',
        'Zemina Torval' => 'torval',

        'Felicia Winters' => 'winters',
        'Zachary Hudson' => 'hudson',

        'Archon Delaine' => 'delaine',
        'Li Yong-Rui' => 'yongrui',
        'Pranav Antal' => 'antal',
        'Yuri Grom' => 'grom'
    ];
    
    function get_powerplay_id($name) {
        if (array_key_exists($name, POWERPLAY_IDS)) {
            return POWERPLAY_IDS[$name];
        } else {
            return 'none';
        }
    }

    const SURFACE_SIGNAL_NAMES = [
        '$SAA_SignalType_Biological;' => 'Biological',
        '$SAA_SignalType_Geological;' => 'Geological',
        '$SAA_SignalType_Guardian;' => 'Guardian',
        '$SAA_SignalType_Human;' => 'Human',
        '$SAA_SignalType_Thargoid;' => 'Thargoid',
        '$SAA_SignalType_Other;' => 'Other',

        'LowTemperatureDiamond' => 'Low Temperature Diamonds',
        'Opal' => 'Void Opals',
        'tritium' => 'Tritium'
    ];
    
    function get_surface_signal_name($key) {
        if (array_key_exists($key, SURFACE_SIGNAL_NAMES)) {
            return SURFACE_SIGNAL_NAMES[$key];
        } else {
            return $key;
        }
    }

    const CG_ACTIVITY_NAMES = [
        "mining" => "Mining",
        "carto" => "Exploration",
        "combatbond" => "Combat bonds",
        "bounty" => "Bounty hunting",
        "research" => "Data",
        "tradelist" => "Trading",
    ];
    
    function get_cg_activity_name($id) {
        if (array_key_exists($id, CG_ACTIVITY_NAMES)) {
            return CG_ACTIVITY_NAMES[$id];
        } else {
            return strval($id);
        }
    }

    const RSS_LANGUAGE_MAP = [
        'en' => 'en-GB',
        'es' => 'es-ES',
        'de' => 'de-DE',
        'fr' => 'fr-FR',
        'ru' => 'ru-RU'
    ];
    
    function get_rss_language($lang) {
        if (array_key_exists($lang, RSS_LANGUAGE_MAP)) {
            return RSS_LANGUAGE_MAP[$lang];
        } else {
            return strval($lang);
        }
    }
    
    function is_discord() {
        return strstr($_SERVER['HTTP_USER_AGENT'], "Discordbot") !== false;
    }

    date_default_timezone_set(DEFAULT_TIMEZONE);