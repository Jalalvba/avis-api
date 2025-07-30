from google.auth import default
from googleapiclient.discovery import build

# Spreadsheet configuration
SPREADSHEET_ID = '15JHCWWX0OPu8BhbNdpsppDO3lDFqDvIEtdc2QCcO1y4'
RANGE_NAME = 'BDD'

# Cloud Run injecte automatiquement les credentials du service account
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials, _ = default(scopes=SCOPES)

def get_sheets_service():
    return build('sheets', 'v4', credentials=credentials)
