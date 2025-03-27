import os
from dotenv import load_dotenv
import streamlit as st

# Import SQLDatabase and SQLDatabaseChain from langchain_experimental
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

# If you have a local HuggingFaceHub from langchain_community, import it:
from langchain_community.llms import HuggingFaceHub

load_dotenv()

class ExcelAnalyser:
    def __init__(self, uri):
        self.uri = uri

    def connect_to_uri(self):
        """
        Connect to the SQLite database and create a simple SQLDatabaseChain
        that can answer questions by generating and running SQL queries.
        """
        # 1) Load the database from the SQLite file
        db = SQLDatabase.from_uri(self.uri)

        # 2) Use an open-source model from Hugging Face (Falcon 7B Instruct example)
        llm = HuggingFaceHub(
            repo_id="tiiuae/falcon-7b-instruct",
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
            model_kwargs={"temperature": 0.1, "max_new_tokens": 64},
        )

        # 3) Create the SQLDatabaseChain with query checking enabled
        chain = SQLDatabaseChain.from_llm(
            llm=llm,
            db=db,
            verbose=True,
            use_query_checker=True
        )
        return chain

def chat_interface():
    st.title("Chat with your Excel Data")
    
    if 'db_path' not in st.session_state:
        st.warning("Please upload an Excel or CSV file first!")
        return

    # Show which tables exist in the database
    db = SQLDatabase.from_uri(st.session_state['db_path'])
    tables = db.get_usable_table_names()
    st.write(f"Available tables: {tables}")
    
    # Maintain a simple chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask questions about your Excel data"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                analyser = ExcelAnalyser(st.session_state['db_path'])
                chain = analyser.connect_to_uri()

                # Use invoke with a dict input instead of run()
                response = chain.invoke({"query": prompt})

                # Display the result
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_message = f"Error: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

if __name__ == '__main__':
    chat_interface()
