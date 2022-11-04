<?php
    require_once 'common.php';
    require_once 'libs/Smarty.class.php';
    
    $changed = false;
    
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $newlang = filter_input(INPUT_POST, 'lang', FILTER_DEFAULT, [
            'options' => [
                'default' => 'en',
            ]
        ]);
        
        if (!in_array($newlang, LANGUAGES, true)) {
            $newlang = 'en';
        }
        
        setcookie('birdnet_language', $newlang);
		$_COOKIE['birdnet_language'] = $newlang;
        $changed = true;
    }
    
    $smarty = new Smarty();
    $smarty->setTemplateDir('tpl');
    $smarty->assign('changed', $changed);
    $smarty->assign('languageIds', LANGUAGES);
    $smarty->assign('languageNames', LANGUAGE_NAMES);
    $smarty->assign('currentLanguage', get_user_language());
    $smarty->assign('defaultLanguage', get_default_language());
    $smarty->display('language.tpl');