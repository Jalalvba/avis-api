import re
from auth import get_sheets_service, SPREADSHEET_ID, RANGE_NAME
from get import get_bdd_data

def normalize_immat(immat):
    return re.sub(r'[^A-Za-z0-9]', '', immat).upper()

def update_row_by_immat(immat, new_row):
    service = get_sheets_service()
    sheet = service.spreadsheets()

    # Normalize the target key
    immat_key = normalize_immat(immat)

    # Fetch existing data
    all_data = get_bdd_data()
    headers = all_data[0]
    rows = all_data[1:]

    # Find row index with normalized match
    try:
        row_index = next(
            i for i, row in enumerate(rows, start=2)
            if normalize_immat(row[0]) == immat_key
        )
    except StopIteration:
        raise Exception(f"Immatriculation '{immat}' not found")

    # Replace row at that position
    update_range = f"{RANGE_NAME}!A{row_index}:G{row_index}"

    body = {
        'values': [new_row]
    }

    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=update_range,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()

    return result
