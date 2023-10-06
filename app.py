import streamlit as st

st.set_page_config(page_title="Ask Xata", page_icon=":butterfly:", menu_items={"Report a Bug": "mailto:seth.roberts@hey.com"})
st.title(':butterfly: Ask Zata')
prompt = st.text_input('Plug in your prompt here')

if prompt:
    st.write(prompt)