import streamlit as st
from upload import main as upload_main
from main import chat_interface

st.set_page_config(page_title="Excel Analysis Chat", layout="wide")

# Create tabs for upload and chat interface.
tab1, tab2 = st.tabs(["Upload Data", "Chat Interface"])

with tab1:
    upload_main()

with tab2:
    chat_interface()
