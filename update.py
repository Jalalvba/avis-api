import re
from auth import get_sheets_service, SPREADSHEET_ID, RANGE_NAME
from get import get_bdd_data

def normalize_immat(immat):
    return re.sub(r'[^A-Za-z0-9]', '', immat).upper()

def update_row_by_immat(immat, new_data_dict):
    service = get_sheets_service()
    sheet = service.spreadsheets()

    immat_key = normalize_immat(immat)
    all_data = get_bdd_data()
    headers = all_data[0]
    rows = all_data[1:]

    try:
        row_index = next(
            i for i, row in enumerate(rows, start=2)
            if normalize_immat(row[0]) == immat_key
        )
    except StopIteration:
        raise Exception(f"Immatriculation '{immat}' not found")

    # Ancienne ligne avant mise à jour
    current_row = rows[row_index - 2]

    # Ne mettre à jour que les champs fournis (sinon garder ancienne valeur)
    updated_row = [
        new_data_dict.get(col, current_row[i]) for i, col in enumerate(headers)
    ]

    update_range = f"{RANGE_NAME}!A{row_index}:G{row_index}"
    body = { 'values': [updated_row] }

    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=update_range,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()

    return {
        "result": result,
        "updated_row": dict(zip(headers, updated_row))
    }
