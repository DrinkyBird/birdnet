import scrape_config
import mariadb
import sys
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import argparse
import datetime

db = mariadb.connect(
    host=scrape_config.DB_HOST,
    user=scrape_config.DB_USER,
    password=scrape_config.DB_PASSWORD,
    database=scrape_config.DB_NAME
)

_BASE_GSHEET_DATE = datetime.date(1899, 12, 30)
_BASE_GSHEET_DATETIME = datetime.datetime(_BASE_GSHEET_DATE.year, _BASE_GSHEET_DATE.month, _BASE_GSHEET_DATE.day)

def convert_datetime_to_gsheet(dt: datetime.datetime, /) -> float:
    # Ref: https://stackoverflow.com/a/66738817/
    assert isinstance(dt, datetime.datetime)
    delta = dt - _BASE_GSHEET_DATETIME
    return delta.days + delta.seconds / 86_400.0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("id", type=int)
    parser.add_argument("progress", type=int)
    parser.add_argument("delta", type=int)
    args = parser.parse_args()
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM `goals_en` WHERE `id`=%s", (args.id,))
    cg = cursor.fetchone()
    cg_now = datetime.datetime.utcfromtimestamp(cg["last_updated"])
    
    if cg is None:
        print("unknown id")
        sys.exit(1)
        
    cursor.execute("SELECT * FROM `goals_sheets` WHERE `goal_id`=%s", (cg["id"],))
    dbsheet = cursor.fetchone()
    
    credentials = service_account.Credentials.from_service_account_file(scrape_config.GOOGLE_SERVICE_ACCOUNT_KEY)
    gsheets = build("sheets", "v4", credentials=credentials)
    
    if dbsheet is None:
        gdrive = build("drive", "v3", credentials=credentials)
        spreadsheet = {
            "properties": {
                "title": f"{cg['id']} - {cg['title']}"
            },
            "sheets": [
                {
                    "properties": {
                        "sheetId": 0,
                        "title": "Progress",
                        "gridProperties": {
                            "columnCount" : 3,
                            "frozenRowCount": 1
                        }
                    },
                    "data": [
                        {
                            "startRow": 0,
                            "startColumn": 0,
                            "rowData": [
                                {
                                    "values": [
                                        {
                                            "userEnteredValue": {
                                                "stringValue": "Timestamp"
                                            },
                                            "userEnteredFormat": {
                                                "textFormat": {
                                                    "bold": True
                                                }
                                            }
                                        },
                                        {
                                            "userEnteredValue": {
                                                "stringValue": "Progress"
                                            },
                                            "userEnteredFormat": {
                                                "textFormat": {
                                                    "bold": True
                                                }
                                            },
                                            "note": "Total progress"
                                        },
                                        {
                                            "userEnteredValue": {
                                                "stringValue": "Delta"
                                            },
                                            "userEnteredFormat": {
                                                "textFormat": {
                                                    "bold": True
                                                }
                                            },
                                            "note": "Contributions since previous update"
                                        }
                                    ]
                                },
                                {
                                    "values": [
                                        {
                                            "userEnteredValue": {
                                                "numberValue": convert_datetime_to_gsheet(cg_now)
                                            },
                                            "userEnteredFormat": {
                                                "numberFormat": {
                                                    "type": "DATE_TIME"
                                                }
                                            }
                                        },
                                        {
                                            "userEnteredValue": {
                                                "numberValue": args.progress
                                            },
                                            "userEnteredFormat": {
                                                "numberFormat": {
                                                    "type": "NUMBER",
                                                    "pattern": "#,###0"
                                                }
                                            }
                                        },
                                        {
                                            "userEnteredValue": {
                                                "numberValue": args.delta
                                            },
                                            "userEnteredFormat": {
                                                "numberFormat": {
                                                    "type": "NUMBER",
                                                    "pattern": "#,###0"
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        spreadsheet = gsheets.spreadsheets().create(body=spreadsheet).execute()
        sheetId = spreadsheet.get('spreadsheetId')
        print("Sheet ID: " + sheetId)
        
        cursor.execute("INSERT INTO `goals_sheets` (`goal_id`, `sheet_id`) VALUES (%s, %s)", (cg["id"], sheetId))
        db.commit()
        
        file = gdrive.files().get(fileId=sheetId, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        gdrive.files().update(fileId=sheetId, addParents=scrape_config.GOOGLE_DRIVE_FOLDER_ID, removeParents=previous_parents).execute()
        
        permission = {
            "type": "anyone",
            "role": "reader"
        }
        
        gdrive.permissions().create(fileId=sheetId, body=permission).execute()
    else:
        sheetId = dbsheet["sheet_id"]
        data = {
            "requests": [
                {
                    "appendCells": {
                        "sheetId": 0,
                        "rows": [
                            {
                                "values": [
                                    {
                                        "userEnteredValue": {
                                            "numberValue": convert_datetime_to_gsheet(cg_now)
                                        },
                                        "userEnteredFormat": {
                                            "numberFormat": {
                                                "type": "DATE_TIME"
                                            }
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "numberValue": args.progress
                                        },
                                        "userEnteredFormat": {
                                            "numberFormat": {
                                                "type": "NUMBER",
                                                "pattern": "#,###0"
                                            }
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "numberValue": args.delta
                                        },
                                        "userEnteredFormat": {
                                            "numberFormat": {
                                                "type": "NUMBER",
                                                "pattern": "#,###0"
                                            }
                                        }
                                    }
                                ]
                            }
                        ],
                        "fields": "*"
                    }
                }
            ],
            "includeSpreadsheetInResponse": False
        }
        gsheets.spreadsheets().batchUpdate(spreadsheetId=sheetId, body=data).execute()
    