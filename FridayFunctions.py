import time as timex
import json
import datetime
import requests, lxml
from google.cloud import speech
from googlesearch import search
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup


def tell_time():
    time_string = timex.strftime("%Y-%m-%d %H:%M:%S", timex.localtime())
    return time_string

def time():
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    return now

def write_to_file():
    file_csv = open('history.csv', 'r')
    file_json = open('history.json', 'w')
    messages = []
    i = 0
    for line in file_csv:
        i += i
        print(f"line: {i}")
        print(line)
        line = line.strip()
        if line:
            message = json.dumps(line)
            dumped_message = json.loads(message)
            print(dumped_message)
            messages.append(dumped_message)
    json.dump(messages, file_json, indent=2)

def search_web(query: str, num_results: int):
    results = []
    for result in search(query, num_results=num_results):
        results.append(result)
    return results

def webpage_open(link: str):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        return soup.prettify()
    except Exception as e:
        return e

def text_document_read(filename: str):
    r'''
    :param filename:
    :return:
    '''
    text = ""
    with open(filename, 'r') as f:
        for line in f:
            text = text + " " + line
    return text

###Google API OAuth2 checkin
SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/calendar.events", "https://www.googleapis.com/auth/gmail.readonly"]

##client_secret_calendar.json is the client secret file obtained from OAuth client ID download file in your API settings
flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret_calendar.json", SCOPES
)
cred = flow.run_local_server(port=0)
# Save the credentials for the next run
with open("token.json", "w") as token:
    token.write(cred.to_json())


def calendar_list_events(calendar_id : str, timeMin : str):
    r'''
    :param calendar_id: The name of the calendar to use, default is "primary"
    :param timeMin: The start time of the events, please put in UTC, you can use the time() function for this as default
    :return: Returns the list of events in the specified calendar
    '''
    service = build("calendar", "v3", credentials=cred)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    try:
        events = service.events().list(calendarId=calendar_id, timeMin=timeMin).execute()

        event_list = []
        for item in events['items']:
            event_list.append(item)
        return event_list

    except HttpError as error:
        print(f"An error occurred: {error}")

def calendar_list_calendars():
    r'''
    :return: returns the list of calendars available for google account
    '''
    page_token = None
    service = build("calendar", "v3", credentials=cred)
    while True:
        calendar_list = service.calendarList().list(pageToken = page_token).execute()
        list = []
        for calendar_list_entry in calendar_list['items']:
            list.append(calendar_list_entry)
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
        return list

def calendar_get_event(calendar_id : str, event_id : str):
    r'''
    :param calendar_id: the name of the calendar to use, default is "primary"
    :param event_id: the name of the event to search for
    :return: returns the event object
    '''
    service = build("calendar", "v3", credentials=cred)

    try:
        event = service.events().get(calendarId = calendar_id, eventId = event_id).execute()

        return event
    except HttpError as error:
        print(f"An error occurred: {error}")

def gmail_read():
    r'''
    :return: Returns the list of message objects including id and snippet
    '''
    try:
        service = build("gmail", "v1", credentials=cred)
        results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
        labels = results.get('messages', [])

        if not labels:
            return "No Labels Found"
        label_list = []
        for item in labels:
            message_raw = service.users().messages().get(userId='me', id=item['id'], format='minimal').execute()
            label_list.append(message_raw)
        return label_list
    except HttpError as error:
        print(f"An error occurred: {error}")


