import streamlit as st
from streamlit_chat import message
from Main import search_db
import time



st.title ('Chat Bot: LAW Consultation')

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    # text = st.empty()
    input_text = st.text_input("Welcome to XYZ Law Firm's Advice Bot! Please ask me anything and I will try my best to answer you! However, please note that the reply I provide is not legal advice. If you require legal advice, please book an appointment with one of our helpful lawyers here! (dummyLink).", key='input')

    return input_text

user_input = get_text()

if user_input:
    with st.spinner('Please wait:'):
        output = search_db(user_input)
        
        output = output.split('AI:')[1]

        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)
        print(output)
        



if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['generated'][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')



    
