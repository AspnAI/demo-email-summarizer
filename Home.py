import streamlit as st
import pandas as pd
import random
from streamlit_modal import Modal
import streamlit.components.v1 as components



# Main app logic
def main():
    st.title("Email Summarizer")
    # csv_file_path = 'new_corrected_support_emails.csv'  # Replace with your CSV file path
    # df = load_data(csv_file_path)

    # # Initialize the session state for page control
    # if 'show_inbox' not in st.session_state:
    #     st.session_state['show_inbox'] = True  # Show inbox by default

    # if st.session_state['show_inbox']:
    #     display_inbox(df)
    # else:
    #     display_reply_page()    

if __name__ == "__main__":
    main()
