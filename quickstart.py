from __future__ import print_function
import os.path
from time import sleep
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.

row = 2

SAMPLE_SPREADSHEET_ID = '1TrBjFW-bFRMBze4ShWvYtB9eFvEyvyW10J_Aoqfw4fQ' #Add the ID of the spreadsheet with you urls and then where you
SAMPLE_RANGE_NAME_SHEET1 = 'Sheet1!A2:A' # Where your URLS begin on the sheets
    
def main():
    service = get_google_service() # connects to your google sheets
    data = get_data(service) # getting the url from the sheets
    data = run_selenium(data) 

    append_values(data, service)

def get_google_service():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('sheets', 'v4', credentials=creds)

def get_data(service):
    try:
         # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME_SHEET1).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        print(values)
        return values
    except HttpError as err:
        print(err)


def run_selenium(data):
    service = Service(executable_path="/path/to/chromedriver")
    driver = webdriver.Chrome(service=service)
    driver.get("https://wordcounter.net/website-word-count")
    input = driver.find_element(By.XPATH, '//*[@id="url"]')
    return_data = []
    for row in data:
        input = driver.find_element(By.XPATH, '//*[@id="url"]')
        input.send_keys(row[0])
        form = driver.find_element(By.XPATH, '/html/body/div[6]/div/form/div/div[2]/input')
        form.click()
        top_word = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div[1]/div/table/tbody/tr[1]/td[1]')
        top_word_inner_html = top_word.get_attribute('innerHTML')
        top_word_count = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div[1]/div/table/tbody/tr[1]/td[2]')
        top_word_count_inner_html = top_word_count.get_attribute("innerHTML")
        total_word_count = driver.find_element(By.XPATH, '//*[@id="word_count_block"]/span')
        total_word_count_inner_html = total_word_count.get_attribute('innerHTML')
        index_to_remove = total_word_count_inner_html.index('<')
        total_word_count_inner_html = total_word_count_inner_html[:index_to_remove]
        arr_to_append = [total_word_count_inner_html, top_word_inner_html, top_word_count_inner_html]
        return_data.append(arr_to_append)
    driver.close()
    return return_data

def append_values(values, service):
    range = f'Sheet1!B2'
    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, 
        range=range, 
        valueInputOption='RAW',
        body={'values': values}
    ).execute()
    # Return the result of the API call
    return result

if __name__ == '__main__':
    main()


