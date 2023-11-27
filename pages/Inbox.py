import streamlit as st
import pandas as pd
import random
from streamlit_modal import Modal
import streamlit.components.v1 as components
from tools import openai
import os


def generate_response(email_body):
    key = st.session_state['current_key']
    summary = st.session_state.get(f'{key}_summary')
    if summary is None:
        summary = email_body
    res = openai.getAIResponse(f"Generate a response to the following email thread for my company keeping in mind the information provided to you. Dont use placeholders, and assume stuff where necessary. Generate Random or Fake data like Names, designations, etc wherever you feel necessary. While writing the email conclusion, use the following format:\
    Best Regards,\
    Julia Smith <Replace this with a random name>\
    Customer Support Executive",
    f"Email Thread: {email_body}\n\nSummary: {summary}\
    My Comapny Information: {st.session_state['company_info']},\
    Sentiment: {st.session_state.get(f'{key}_sentiment')},\
    Priority: {st.session_state.get(f'{key}_priority')}\
    Category: {st.session_state.get(f'{key}_category')}\
    ")
    return res

# Load the CSV file

@st.cache_data
def load_data(csv_file, support_email):
    print(f"SUPPORT EMAIL: {support_email}")
    df = pd.read_csv(csv_file)
    df['To'] = df['To'].str.strip().str.lower()
    df['From'] = df['From'].str.strip().str.lower()
    inbound_emails = df[df['To'] == support_email]
    replies = df[df['From'] == support_email]
    # Match replies with inbound emails to create threads
    threads = []
    print(df)
    for i, inbound in inbound_emails.iterrows():
        reply = replies[replies['From']
                        == inbound['To']]
        thread = {
            'From': inbound['From'],
            'Subject': inbound['Subject'],
            'Inbound_Body': inbound['Body'],
            'Reply_Body': reply.iloc[i]['Body'] if not reply.empty else "No reply yet",
            'Category': inbound['Category'],
            'Sentiment': inbound['Sentiment'],
            'Priority': inbound['Priority']
        }
        threads.append(thread)
    print(f"Created {len(threads)} threads")
    return pd.DataFrame(threads)



def display_inbox(df):
    for index, row in df.iterrows():
        print(row)
        col1, col2, col3,col4 = st.columns([2, 1, 1, 1])
        with col1:
            st.write(f"From: {row['From']}")
            st.write(f"Subject: {row['Subject']}")
        with col2:
            st.write(f"**Category:** {row['Category']}")
        with col3:
            st.write(f"**Sentiment:** {row['Sentiment']}")
        with col4:
            priority = row['Priority']
            if row['Category'] == 'Spam' or row['Category'] == 'Notification':
                priority = 'Low'

            if not priority:
                priority = random.choice(['High', 'Medium', 'Low'])
            if priority == 'High':
                st.write(f"<span style='color: darkred; background-color: lightcoral; padding: 2px 6px; border-radius: 0.5rem '>**Priority:** {priority}</span>", unsafe_allow_html=True)
            elif priority == 'Medium':
                st.write(f"<span style='color: darkgoldenrod; background-color: lightyellow;padding: 2px 6px; border-radius: 0.5rem '>**Priority:** {priority}</span>", unsafe_allow_html=True)
            elif priority == 'Low':
                st.write(f"<span style='color: darkgreen; background-color: lightgreen;padding: 2px 6px; border-radius: 0.5rem '>**Priority:** {priority}</span>", unsafe_allow_html=True)

        # Now the expander just for the email body
        with st.expander("Show Email Thread"):
            st.write(f"Inbound Email: {row['Inbound_Body']}")
            st.divider()
            st.write(f"Reply: {row['Reply_Body']}")
            st.divider()
            thread_summary_key = f"show_summary_{index}"

            # Initialize the session state for this thread summary if not already done
            if thread_summary_key not in st.session_state:
                st.session_state[thread_summary_key] = False

            # Button to toggle thread summary
            if st.button("Thread Summary", key=f"btn_summary_{index}"):
                # Toggle the state
                st.session_state[thread_summary_key] = not st.session_state[thread_summary_key]

            # Show or hide the thread summary based on the state
            if st.session_state[thread_summary_key]:
                with st.spinner('Generating thread summary...'):
                    summary = generate_thread_summary(
                        row['Inbound_Body'], row['Reply_Body'], index)
                    st.write(summary)

            #####################################################################
            # Reply form

            if st.button("Generate Reply", key=f"btn_reply_{index}"):
                # Go to a new page with the inbound email and a form field with a suggested response
                st.session_state['current_key'] = index
                st.session_state['current_email'] = row['Inbound_Body']
                st.session_state['show_inbox'] = False
                st.session_state[f'{index}_sentiment'] = row['Sentiment']
                st.session_state[f'{index}_priority'] = row['Priority']
                st.session_state[f'{index}_category'] = row['Category']
                st.rerun()


# Simulated function to generate a thread summary that takes some time
def generate_thread_summary(inbound_body, reply_body, key):
    summary = openai.summarizeEmailThread(
        f"Inbound: {inbound_body}\n\nResponse: {reply_body}")
    st.session_state[f'{key}_summary'] = summary
    return summary
    # return f"Inbound: {inbound_body}\n\nResponse: {reply_body}"

# Display the email reply page


def display_reply_page():
    if 'current_email' in st.session_state:
        st.write(st.session_state['current_email'])
        suggested_response = generate_response(st.session_state['current_email'])
        response = st.text_area("Your Response", value=suggested_response)

        if st.button("Send Response"):
            st.success("Response sent!")

        # Back button to return to the inbox
        if st.button("Back to Inbox"):
            st.session_state['show_inbox'] = True
            st.rerun()
    else:
        st.warning("No email selected.")


st.title("Inbox")
# Replace with your CSV file path
csv_file_path = 'emails_data.csv'
if os.path.exists(csv_file_path) == False:
    st.warning("Please set the CSV file path in the code.")
else:
    # Load the CSV file
    if 'support_email' in st.session_state:
        support_email = st.session_state['support_email']
    else:
        # load from text file
        with open("support.txt", "r") as f:
            support_email = f.read()

    if 'company_info' in st.session_state:
        company_info = st.session_state['company_info']
    else:
        # load from text file
        with open("company_info.txt", "r") as f:
            company_info = f.read()
    df = load_data(csv_file_path, support_email)


# Initialize the session state for page control
if 'show_inbox' not in st.session_state:
    st.session_state['show_inbox'] = True  # Show inbox by default

if st.session_state['show_inbox'] and os.path.exists(csv_file_path) != False:
    display_inbox(df)
else:
    display_reply_page()
