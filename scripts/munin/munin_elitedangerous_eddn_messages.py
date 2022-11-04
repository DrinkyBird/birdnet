#!/usr/bin/env python3

import json
import os
import sys
import time
import mysql.connector

ENABLE_TEST_SCHEMAS = False

EDDN_SCHEMAS = [
	'https://eddn.edcd.io/schemas/approachsettlement/1',
	'https://eddn.edcd.io/schemas/approachsettlement/1/test',
	'https://eddn.edcd.io/schemas/blackmarket/1',
	'https://eddn.edcd.io/schemas/blackmarket/1/test',
	'https://eddn.edcd.io/schemas/codexentry/1',
	'https://eddn.edcd.io/schemas/codexentry/1/test',
	'https://eddn.edcd.io/schemas/commodity/3',
	'https://eddn.edcd.io/schemas/commodity/3/test',
	'https://eddn.edcd.io/schemas/fssallbodiesfound/1',
	'https://eddn.edcd.io/schemas/fssallbodiesfound/1/test',
	'https://eddn.edcd.io/schemas/fssbodysignals/1',
	'https://eddn.edcd.io/schemas/fssbodysignals/1/test',
	'https://eddn.edcd.io/schemas/fssdiscoveryscan/1',
	'https://eddn.edcd.io/schemas/fssdiscoveryscan/1/test',
	'https://eddn.edcd.io/schemas/fsssignaldiscovered/1',
	'https://eddn.edcd.io/schemas/fsssignaldiscovered/1/test',
	'https://eddn.edcd.io/schemas/journal/1',
	'https://eddn.edcd.io/schemas/journal/1/test',
	'https://eddn.edcd.io/schemas/navbeaconscan/1',
	'https://eddn.edcd.io/schemas/navbeaconscan/1/test',
	'https://eddn.edcd.io/schemas/navroute/1',
	'https://eddn.edcd.io/schemas/navroute/1/test',
	'https://eddn.edcd.io/schemas/outfitting/2',
	'https://eddn.edcd.io/schemas/outfitting/2/test',
	'https://eddn.edcd.io/schemas/scanbarycentre/1',
	'https://eddn.edcd.io/schemas/scanbarycentre/1/test',
	'https://eddn.edcd.io/schemas/shipyard/2',
	'https://eddn.edcd.io/schemas/shipyard/2/test'
]

db = mysql.connector.connect(
    host=os.getenv('dbhost'),
    user=os.getenv('dbuser'),
    password=os.getenv('dbpass'),
    database=os.getenv('dbname')
)

def filter_id(label):
    label = label.replace('https://eddn.edcd.io/schemas/', '')
    label = label.replace('/', '_')
    return label.lower()

def filter_label(label):
    label = label.replace('https://eddn.edcd.io/schemas/', '')
    return label

def output_config():
    cursor = db.cursor()
    cursor.execute("SELECT `schema_ref` FROM `eddn_messages` GROUP BY `schema_ref`")
    
    refs = EDDN_SCHEMAS.copy()
    for row in cursor:
        if row[0] not in refs:
            refs.append(row[0])
    
    print("graph_title EDDN messages by schema")
    print("graph_category elitedangerous")
    print("graph_vlabel messages/minute")
    print("update_rate " + str(1 * 60))
    for n in refs:
        id = filter_id(n)
        label = filter_label(n)
        print(f"{id}.label {label}")
        print(f"{id}.min 0")
        print(f"{id}.draw AREASTACK")
        
def output_values():
    start_time = int(time.time() - 60)
    cursor = db.cursor()
    
    result = {}
    for ref in EDDN_SCHEMAS:
        result[filter_id(ref)] = 0
    
    cursor.execute("SELECT `schema_ref`, COUNT(*) FROM `eddn_messages` WHERE `listener_timestamp` >= %s GROUP BY `schema_ref`", (start_time,))
    
    for row in cursor:
        schema = filter_id(row[0])
        value = row[1]
        result[schema] = value
    
    for schema in result:
        value = result[schema]
        print(f"{schema}.value {value}")

if __name__ == "__main__":
    if not ENABLE_TEST_SCHEMAS:
        copy = []
        for s in EDDN_SCHEMAS:
            if not s.endswith('/test'):
                copy.append(s)
        EDDN_SCHEMAS = copy
    
    if len(sys.argv) >= 2:
        if sys.argv[1] == "config": 
            output_config()
    else: 
        output_values()
        