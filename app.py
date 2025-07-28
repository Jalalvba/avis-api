from google.auth import default
from googleapiclient.discovery import build

# Authenticate using Application Default Credentials
credentials, project = default()

# Initialize the Sheets API client
service = build("sheets", "v4", credentials=credentials)

# Your Spreadsheet ID (from the URL)
spreadsheet_id = "15JHCWWX0OPu8BhbNdpsppDO3lDFqDvIEtdc2QCcO1y4"

# The tab name and range you want to read from
range_name = "BDD!A1:E20"  # Adjust range if needed

# Make the API call
response = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range=range_name
).execute()

values = response.get("values", [])

# Print the data
if not values:
    print("❌ No data found in BDD sheet.")
else:
    print("✅ Data from 'BDD' sheet:")
    for row in values:
        print(row)
