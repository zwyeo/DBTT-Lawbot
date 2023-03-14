# Requirements:

- python version need to be 3.10 for streamlit to run
  ## python -V
- create a virtual envrionment and install all the neccessary packages
  - python3 -m venv venv
  - . ./venv/bin/activate (for Mac)
  - venv\Scripts\activate.bat (for Win)
  - pip install -r requirements.txt

# To note:

- openai and langchain may need to be updated if there is error
  - pip install openai --upgrade
  - pip istall langchain --upgrade
- Please change your db path according to ur OS
  - Mac db path is 'db//'
  - Win db path is 'db\\'

# To start the Chatbot:

- streamlit run chatbot.py
