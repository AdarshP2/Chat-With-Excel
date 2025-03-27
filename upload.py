from sqlalchemy import create_engine
import pandas as pd
import streamlit as st

def main():
    uploaded_file = st.file_uploader('Upload your Excel sheets')
    if uploaded_file:
        # Create a SQLite database file from the uploaded file.
        engine = create_engine(f"sqlite:///{uploaded_file.name}.db")
        st.session_state['db_path'] = f"sqlite:///{uploaded_file.name}.db"
        file_type = uploaded_file.name.split(".")[-1]
    
        if file_type == "csv":
            df = pd.read_csv(uploaded_file)
            table_name = st.text_input("Enter table name for CSV", "csv_table")
            if st.button("Save CSV to Database"):
                df.to_sql(table_name, con=engine, if_exists="replace", index=False)
                st.success(f"CSV data has been saved to the '{table_name}' table in the SQLite database.")
    
        elif file_type == "xlsx":
            xls = pd.ExcelFile(uploaded_file)
            sheets = xls.sheet_names
            st.write("Sheets found in Excel file:", sheets)
            for sheet_name in sheets:
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                table_name = st.text_input(f"Enter table name for sheet '{sheet_name}'", sheet_name)
                if st.button(f"Save '{sheet_name}' to Database"):
                    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
                    st.success(f"Sheet '{sheet_name}' has been saved to the '{table_name}' table in the SQLite database.")

if __name__=='__main__':
    main()
