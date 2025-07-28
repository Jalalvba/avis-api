from google.oauth2 import service_account
from googleapiclient.discovery import build

# Spreadsheet configuration
SPREADSHEET_ID = '15JHCWWX0OPu8BhbNdpsppDO3lDFqDvIEtdc2QCcO1y4'
RANGE_NAME = 'BDD'

# Auth setup
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

def get_sheets_service():
    return build('sheets', 'v4', credentials=credentials)
