from auth import get_sheets_service, SPREADSHEET_ID, RANGE_NAME

def get_bdd_data():
    service = get_sheets_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()
    return result.get("values", [])
