# Requirements:

- python version need to be 3.10 for streamlit chatbot to run
  python -V to check the python version

- create a virtual envrionment and install all the neccessary packages
  - python3 -m venv venv
  - . ./venv/bin/activate (for Mac)
  - venv\Scripts\activate.bat (for Win)
  - pip install -r requirements.txt

# To note:

- openai and langchain may need to be updated if there is error
  - pip install openai --upgrade
  - pip istall langchain --upgrade
- Please change your db path according to ur OS in Main.py
  - Mac db path is 'db//'
  - Win db path is 'db\\'

Please also do not share or spam the API.
** The chatbot responses are currently limited to what we put in the database.
When you first start the app for the first time, it will take awhile for the chatbot to generate a response. Subsequent responses will be much faster.
**

## To start the app:

- streamlit run chatbot.py
