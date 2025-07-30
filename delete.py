from auth import get_sheets_service, SPREADSHEET_ID, RANGE_NAME
from get import get_bdd_data
from update import normalize_immat  # reuse same logic

def delete_row_by_immat(immat):
    service = get_sheets_service()
    sheet = service.spreadsheets()

    # Normalise l'immatriculation
    immat_key = normalize_immat(immat)

    # Récupère les données
    all_data = get_bdd_data()
    headers = all_data[0]
    rows = all_data[1:]

    # Cherche la ligne correspondante
    try:
        row_index = next(
            i for i, row in enumerate(rows, start=2)
            if normalize_immat(row[0]) == immat_key
        )
    except StopIteration:
        raise Exception(f"Immatriculation '{immat}' not found")

    # Supprime la ligne via batchUpdate
    body = {
        "requests": [
            {
                "deleteDimension": {
                    "range": {
                        "sheetId": 1647192638,  # ✅ Correct ID for your 'BDD' sheet
                        "dimension": "ROWS",
                        "startIndex": row_index - 1,
                        "endIndex": row_index
                    }
                }
            }
        ]
    }

    response = sheet.batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body=body
    ).execute()

    return response
