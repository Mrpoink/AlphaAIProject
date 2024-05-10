import textwrap
import fitz
import PIL.Image
from APIGEN import model
from APIGEN import modeli
from IPython.display import Markdown

def to_markdown(text):
    text = response.text
    text = text.replace('•', ' *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


chat = model.start_chat(history=[])


print("Welcome to Gemini, Please enter the prompt or menu for menu options")
print("As always, you can enter q to quit at any time!")


while True:
    userin = input("Enter prompt: ")
    if userin == "q":
        exit()

    elif userin == "men":
        print("Image")
        print("Document Scanner")
        menin = input("Enter: ")
        if menin == "Image":
            user_prom = input("Enter Prompt: ")
            user_file = input("Enter file path: ")
            if "'" in user_file:
                user_file = user_file.replace("'", "")
            img = PIL.Image.open(user_file)
            response = modeli.generate_content([user_prom, img], stream=True)
            response.resolve()
            to_markdown(response.text)
        elif menin == "Document Scanner":
            whole = ""
            user_prom1 = input("Enter Prompt: ")
            user_file1 = input("Enter file path: ")
            if "'" in user_file1:
                user_file1 = user_file1.replace("'", "")
            with fitz.open(user_file1) as doc:
                for page in doc:
                    rekt = page.get_text()
                    whole = whole + rekt
                    rektwhole = user_prom1 + ": " + whole
                    response = model.generate_content(rektwhole)

    else:
        response = chat.send_message(userin, stream=True)

    if response == ValueError:
        response.prompt_feedback()
        break
    else:
        for chunk in response:
            print(chunk.text)
        print("_"*80)
        to_markdown(response)
