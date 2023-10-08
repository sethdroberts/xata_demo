import os
import streamlit as st
from xata.client import XataClient
 
#Authenticates Xata. Make sure to unhide Streamlit secrets access when deploying
os.environ['XATA_API_KEY'] = st.secrets['XATA_API_KEY']
api_key = os.environ['XATA_API_KEY']

os.environ['EGW_DB_URL'] = st.secrets['EGW_DB_URL']
db_url = os.environ['EGW_DB_URL']

xata = XataClient(api_key=api_key, db_url=db_url)

#OpenAI prompt
def result_prompt(prompt):
    result = xata.data().ask(
    "egw_cota",
    prompt,
    [
        "When you give an example, this example must exist exactly in the context given.",
        "Only answer questions that are relating to the defined contexts. If asked about a question outside of the context, you can respond with \"It doesn't look like I have enough information to answer that.\"",
    ],
    options={
        "searchType": "keyword",
        "search": {
        "fuzziness": 1,
        "prefix": "phrase",
        "target": "content",
        }
    }
    )
    return result


#General page details
st.set_page_config(page_title="Ask Ellen White", page_icon=":butterfly:", menu_items={"Report a Bug": "mailto:seth.roberts@hey.com"})
st.title(':butterfly: Ask Ellen White')
st.markdown(":wave: Hi!  Welcome to **Ask Ellen White** -- a generative AI search engine based on the full text of *Steps to Christ* \
            and the *Conflict of the Ages* series.\
             :point_left: **Click on the sidebar** for more details about how it works.")
st.write("")
prompt = st.text_input('Enter your prompt here:')

# Sidebar content
with st.sidebar:
    st.header('How does the app work in plain English?')
    st.write('When you submit a question, the app searches a database (containing the full text of the Conflict of the Ages \
             series and Steps to Christ) for \
             paragraphs that seem similar to your question. It sends the top three paragraphs to OpenAI (the platform that \
             powers ChatGPT) and instructs it to answer the question you entered using the paragraphs it found.')
    st.header('Is this open-source? Can I access the code?')
    st.write('Yes, it is! All code used for the app is licensed under the MIT license, which basically means you can \
             do whatever you want with it. [Click here to access the Github repository.](https://github.com/sethdroberts/xata_demo)')
    st.header('Is this authorized by the White Estate?')
    st.write("No, it is not an official or authorized application. However, copyrights on US works published prior to 1928, \
             including the full text of *Steps to Christ*, *Patriarchs and Prophets*, *Prophets and Kings*, *Desire of Ages*, and the \
             *Great Controversy* used in this app, are currently in the public domain.")
    st.header('How does the technical side of the app work?')
    st.markdown("The front-end of the app (the text, prompt bar, etc.) is built in Python using Streamlit. \
                I used a Python-based web scraper equipped with Beautiful Soup to load a Xata serverless database \
                with the following schema for each paragraph of Steps to Christ: book name, paragraph content, paragraph \
                reference, & chapter url.") 
    st.markdown("I then used Xata's **ask** functionality to build the generative AI component. \
                When a prompt is submitted, Xata completes a full-text search of the database (filtered to search paragraph \
                content only), identifies the highest-scoring paragraphs, and sends them to OpenAI via the Xata API as context \
                for the prompt. OpenAI's response includes the database ID's for each paragraph referenced.") 
    st.markdown("I display the generated \
                response and use some Python combined with Streamlit's magic to display the referenced paragraphs, along with links to the full quote context.") 

if prompt:
    with st.spinner('Wait for it...'):
        #Get result from OpenAI and write it
        result = result_prompt(prompt)
        st.write(result['answer'])

        st.subheader("References:")

        #Get ID's for each reference
        sources = result['records']
        reference = xata.records().get("egw_cota", sources[0])
        
        source_n = 1
        for i in sources:
            #Get individual record of reference
            reference = xata.records().get("egw_cota", i)
            page = reference['ref']
            page_name = "Source " + str(source_n) + ": " + reference['book'] + ", pg. " + str(page)

            #Add url and text of reference in a dropdown menu
            with st.expander(page_name):
                page = reference['ref']
                content = reference['content'] + " - " + reference['book'] + ", pg. " + str(page)
                st.info(content)
                context = "Read the context: " + reference['ref_url']
                st.info(context)
            source_n = source_n + 1