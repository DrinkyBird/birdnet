<?php
    $tempAttributesGrouped = [
        "Ships" => [
            138 => "Adder",
            272 => "Alliance Challenger",
            266 => "Alliance Chieftain",
            275 => "Alliance Crusader",
            173 => "Anaconda",
            19 => "Asp Explorer",
            195 => "Asp Scout",
            191 => "Beluga Liner",
            21 => "Cobra Mk III",
            189 => "Cobra Mk IV",
            171 => "Diamondback Explorer",
            172 => "Diamondback Scout",
            192 => "Dolphin",
            20 => "Eagle",
            199 => "Federal Assault Ship",
            194 => "Federal Corvette",
            27 => "Federal Dropship",
            198 => "Federal Gunship",
            140 => "Fer-de-Lance",
            28 => "Hauler",
            139 => "Imperial Clipper",
            177 => "Imperial Courier",
            193 => "Imperial Cutter",
            197 => "Imperial Eagle",
            190 => "Keelback",
            270 => "Krait Mk II",
            277 => "Krait Phantom",
            276 => "Mamba",
            137 => "Orca",
            26 => "Python",
            25 => "Sidewinder",
            260 => "Type-10 Defender",
            134 => "Type-6 Transporter",
            135 => "Type-7 Transporter",
            136 => "Type-9 Heavy",
            24 => "Viper Mk III",
            196 => "Viper Mk IV",
            133 => "Vulture",
        ],

        "Vehicles" => [
            212 => "SRV Scarab",
            369 => "SRV Scorpion",
        ],

        "Fighters" => [
            209 => "Gu-97",
            211 => "Taipan",
            210 => "F63 Condor",
        ],

        "Weapons" => [
            318 => "Karma P-15",
            319 => "Manticore Executioner",
            320 => "Manticore Oppressor",
            321 => "Manticore Intimidator",
            322 => "Manticore Tormentor",
            323 => "TK Aphelion",
            324 => "TK Eclipse",
            325 => "TK Zenith",
            326 => "Karma L-6",
            327 => "Karma AR-50",
            328 => "Karma C-44"
        ],

        "Suits" => [
            313 => "Flight Suit",
            314 => "Artemis Suit",
            315 => "Dominator Suit",
            316 => "Maverick Suit",
        ],

        "Fleet Carriers" => [
            297 => "Drake-class Carrier",
        ],

        "Colour" => [
            67 => "Black",
            70 => "Blue",
            62 => "Gold",
            66 => "Green",
            65 => "Grey",
            64 => "Orange",
            215 => "Pink",
            161 => "Purple",
            69 => "Red",
            63 => "White",
            68 => "Yellow",
            214 => "Cyan",
            204 => "Corroded",
            267 => "(?)Brass",
            268 => "(?)Bronze",
            269 => "(?)Malachite",
            271 => "(?)Copper",
            158 => "(?)Tactical Red",
            160 => "(?)Brown",
            295 => "Gleam",
            296 => "Unknown attribute 296",
            293 => "Stygian"
        ],

        "Type" => [
            178 => "Dashboard",
            179 => "Decal",
            180 => "Paint Job",
            203 => "Ship Kit",
            216 => "CMDR Customisation",
            250 => "Name Plate",
            252 => "Detailing",
            265 => "COVAS",
            298 => "Carrier Layout",
            299 => "Carrier Paint Job",
            312 => "Suit Customisation",
            300 => "Carrier Detailing",
            301 => "Carrier ATC",
            317 => "Weapon Customisation",
        ],
    ];

    foreach ($tempAttributesGrouped as $group => $values) {
        if (is_array($values)) {
            asort($values);
            $tempAttributesGrouped[$group] = $values;
        }
    }

    define("STORE_ATTRIBUTES_GROUPED", $tempAttributesGrouped);

    $tempAttributes = [];

    foreach (STORE_ATTRIBUTES_GROUPED as $group => $values) {
        if (is_array($values)) {
            foreach ($values as $id => $desc) {
                $tempAttributes[$id] = $desc;
            }
        } else {
            $tempAttributes[$group] = $values;
        }
    }

    define("STORE_ATTRIBUTES", $tempAttributes);

    function get_store_attribute_name($id) {
        if (array_key_exists($id, STORE_ATTRIBUTES)) {
            return STORE_ATTRIBUTES[$id];
        } else {
            return strval($id);
        }
    }