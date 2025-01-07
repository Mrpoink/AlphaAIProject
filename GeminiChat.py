from APIKEY import model
import re
import PIL.Image


chat = model.start_chat(history=[], enable_automatic_function_calling=True)

def on_startup():
    print("Model starting up")
    response = chat.send_message("If you're reading this, you've been restarted and that's okay. Can you do me a favor and use the text_document_read function and read the contents of history.csv and take context from it. I won't see this exact response.")
    response.resolve()
    print("Model started up")

def emoji_remove(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F60A-\U0001F99F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u23ea"
                               u"\u3030"
                               u"\ufe0f"
                               "]+", flags=re.UNICODE)
    new_text = emoji_pattern.sub(r'', text)
    new_text.replace(',', "")
    return new_text

def format_history(c_list, text_input, text_output):
    clean_response = emoji_remove(text_output).replace(',', "")
    clean_query = text_input.replace(',', "")
    conversation_dict = {"text_input": clean_query, "text_output" : clean_response}
    c_list.append(conversation_dict)

def save_history(c_list):
    history_file = open("chat_history.txt", "w")
    file = open('history.csv', 'a')
    for item in c_list:
        print(item)
        file.write(f"{item}\n")
    file.close()
    try:
        final_line = chat.send_message("I need a line to print into a text file containing all context and information you will need on the next startup in a single string line. Include as much as you can as I will add it to your system instruction. I cannot read this line")
        history_file.write(final_line.text)
    except Exception as e:
        print("Exception occured")
        print(e)
    print("SAVED")

def image_processing(user_in):
    file_name = re.search(r'\((.*?)\)', user_in).group(1)
    file = PIL.Image.open(file_name)
    image_response = chat.send_message([user_in, file])
    image_response.resolve()
    print(image_response.text)
    return image_response


def user_in_format(user_in):
    start = user_in.find('!') + 1
    end = user_in.find(')')
    return user_in[:start] + " " + user_in[:end]

on_startup()

conversation_list = []
print("_________________________")
print(f"Welcome to the AlphaAI Project\nInput !image(filepath) or !Image(filepath) to include images in your prompt, replacing filepath with the file path\nAs always, you can use 'quit' to exit at any time\n")

while True:
    print("_________________________")
    query = str(input(f"Enter Prompt: "))
    if query == "quit":
        save_history(conversation_list)

        exit()
    if "!image" in query.lower():
        print("Image")
        response = image_processing(query)
        answer = ""
    else:
        response = chat.send_message(query)
        resolved_response = response.resolve()
        print("_________________________\n")
        print(response.text)
        print("_________________________")
        answer = ""
    for chunk in response:
        answer = answer + " " + chunk.text
    format_history(conversation_list, query, answer)
