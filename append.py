from auth import get_sheets_service, SPREADSHEET_ID, RANGE_NAME

def append_row_to_bdd(row):
    service = get_sheets_service()
    sheet = service.spreadsheets()

    body = {
        'values': [row]  # Must be a list of lists
    }

    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

    return result
