import os
import streamlit as st
from xata.client import XataClient
 
#Authenticates Xata. Make sure to unhide Streamlit secrets access when deploying
os.environ['XATA_API_KEY'] = st.secrets['XATA_API_KEY']
api_key = os.environ['XATA_API_KEY']

os.environ['EGW_DB_URL'] = st.secrets['EGW_DB_URL']
db_url = os.environ['EGW_DB_URL']

xata = XataClient(api_key=api_key, db_url=db_url)

st.set_page_config(page_title="Ask Xata", page_icon=":butterfly:", menu_items={"Report a Bug": "mailto:seth.roberts@hey.com"})
st.title(':butterfly: Ask Zata')
prompt = st.text_input('Plug in your prompt here')

if prompt:
    results = xata.data().search_branch({"query": prompt})
    st.write(results)

    