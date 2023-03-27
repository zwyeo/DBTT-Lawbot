import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Home",
    page_icon=":house:",
    layout="wide"
)
st.sidebar.success("Select a page above.")

# st.header("Home")

import streamlit.components.v1 as components

# embed streamlit docs in a streamlit app
# components.iframe("https://edenlaw.com.sg/articles/", width=1000, height=800)
st.markdown(
    """
    <style>
    .wrapper {
      position: relative;
      width: 100%;
      height: 0;
      padding-bottom: 56.25%;
    }

    .wrapper iframe {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

url = 'https://edenlaw.com.sg/articles/'
st.markdown(f'<div class="wrapper"><iframe src="{url}"></iframe></div>', unsafe_allow_html=True)






