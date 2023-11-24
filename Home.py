import streamlit as st
import pandas as pd
import random
from streamlit_modal import Modal
import streamlit.components.v1 as components
import streamlit_scrollable_textbox as stx

from tools import scraper
from tools import openai

# Main app logic
def main():
    st.title("Email Summarizer")
    st.subheader("Summarize your emails with ease")

    st.divider()

    st.subheader("Your company website to generate context")
    website_url = st.text_input("Enter website:", value="", max_chars=None, key=None, type="default",
                   help=None, autocomplete=None, on_change=None, args=None, kwargs=None,
                   placeholder="https://www.example.com", disabled=False, label_visibility="visible")
    
    scrape_button = st.button("Scrape", key=None, help=None, on_click=None, args=website_url, kwargs=None,type="primary", disabled=False, use_container_width=False)

    st.divider()

    if scrape_button:
        try:
            website_text=scraper.getWebsiteText(website_url)
            st.session_state['website_text'] = website_text
        except:
            st.write("Please enter a valid URL (that is scrapeable with requests)")
        st.subheader("Website Text")
        stx.scrollableTextbox(website_text)

        st.subheader("Company information")
        company_info = openai.getAIResponse(
            "Determine company industry, and products or service.\
            If you cannot determine the service then assume it is a consulting service.",
            website_text
        )
        st.session_state['company_info'] = company_info
        st.write(company_info)




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
