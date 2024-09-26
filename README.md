# AlphaAIProject

This is an AI project built off Google's Gemini Generative Language Model  
***THIS MODEL CANNOT RUN ON x32 CPUS, TRUST ME I TRIED***  

VERSION 1.3 IS AVAILABLE!!
* rewritten the entire Attempt.py to now be GeminiChat.py as the start
* Friday Functions! (tell_time, web_search, webpage_open, text_document_read, write_file)
* Friday Memory!! Friday can gain context from a history.csv file that contains all conversation history which should be automatically created and written to


Please keep in mind this is NOT a comprehensive guide to installation or usage, although I will provide links to guides I follow, and so can you if you wish to build this project for yourself.
I designed Friday for me, I just thought I would hand out the source code so people can develop their own Friday, or whatever they'd like to name it. 
Friday can be run using any command line tool that runs Python. 
It was created to be a tool that can be used almost instantaneously to do anything Gemini can do but in a more customizable way so users can do anything they want with it within the parameters Google
has given us. 

Installation - https://ai.google.dev/gemini-api/docs/quickstart (Google's Python Quickstart Guide)   
***(I will try to make a bash file to install all this stuff)***

Create API Key from Google (https://ai.google.dev/gemini-api/docs/quickstart#set-up-api-key)

sudo apt install python3-pip  
sudo apt install python3-venv

pip install -U google-generativeai

***(If you cannot get AlphaAI to work on your machine then you might need to make a venv and build the packages and dependencies yourself and copy over the python files I've created)***

