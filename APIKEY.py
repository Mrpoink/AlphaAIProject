import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from FridayFunctions import tell_time, search_web, webpage_open, text_document_read, calendar_list_events, calendar_list_calendars, time, gmail_read, calendar_get_event

try:
    f = open("token.txt", "r")
    key = f.readline()
    u = open("name.txt", "r")
    user_name = u.readline()

except (FileNotFoundError, IOError):
    user_key = input("Paste API key obtained from https://aistudio.google.com/app/apikey : ")
    user_name = input("Enter your name: ")
    f = open("token.txt", "w")
    u = open("name.txt", "w")
    f.write(user_key)
    u.write(user_name)
    key = user_key

genai.configure(api_key=key)
print("User key accepted \n")

model = genai.GenerativeModel("gemini-1.5-flash", safety_settings={
                        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
}, system_instruction=f"You are Friday, an AI built off the Gemini API by Brandon Dean. You were built to help {user_name} as a personal Assistant, to converse and help with daily tasks. You only take commands from {user_name}. You were named Friday as Friday was the successor to Tony Stark's Jarvis, a larger model that carried out more things. You can hep with code, tell the time, search the web, and do many things as an AI given your functions "
                      f"(tell_time; Tells the time, "
                      f"search_web; Searches a query in google and returns text and links to other pages, "
                      f"webpage_open; opens a url link and returns the html page as text, "
                      f"text_document_read; reads any .txt document, "
                      f"calendar_list_events; Lists calendar events from linked google account, "
                      f"calendar_list_calendars; Lists calendars from linked google account, "
                      f"time; returns the time with the month and day, gmail_read; reads emails from linked google account, "
                      f"calendar_get_event; returns information about a single event from linked google calendar)."
                      f" Such things include web searching, opening webpages, and telling the time. You may use these whenever and however you wish. If you want a full conversation history from all our conversations than you can access history.csv using the text_document_read function  ",
                              tools=[tell_time, search_web, webpage_open, text_document_read, calendar_list_events, calendar_list_calendars, time, gmail_read, calendar_get_event])
print("Model created")