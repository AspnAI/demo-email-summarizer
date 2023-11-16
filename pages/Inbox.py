import streamlit as st
import pandas as pd
import random
from streamlit_modal import Modal
import streamlit.components.v1 as components


# Function to generate a random sentiment
def generate_sentiment():
    return "positive" if random.random() > 0.5 else "negative"

# Function to generate a random priority
def generate_priority():
    priorities = ["low", "medium", "high"]
    return random.choice(priorities)

# Function to simulate generating a response with LangChain
def generate_response(email_body):
    # This is where you'd integrate with a language model or an API
    return "This is a simulated response. Replace this function with your LangChain call."

# Load the CSV file
@st.cache_data
def load_data(csv_file):
    df = pd.read_csv(csv_file)

    # Separate inbound emails and replies
    inbound_emails = df[df['To'] == 'support@aspn.ai']
    replies = df[df['From'] == 'support@aspn.ai']

    # Match replies with inbound emails to create threads
    threads = []
    for _, inbound in inbound_emails.iterrows():
        # Find the reply for this inbound email
        reply = replies[replies['To'] == inbound['From']]
        if not reply.empty:
            thread = {
                'From': inbound['From'],
                'Subject': inbound['Subject'],
                'Inbound_Body': inbound['Body'],
                'Reply_Body': reply.iloc[0]['Body'] if not reply.empty else "No reply yet"
            }
            threads.append(thread)
    
    return pd.DataFrame(threads)

# Display the inbox
def display_inbox(df):
    for index, row in df.iterrows():
    #     with st.expander(f"{row['From']} - {row['Subject']}"):
    #         st.write(row['Body'][:100])  # Show a snippet of the body
    #         st.markdown(f"**Category:** Support")
    #         st.markdown(f"**Sentiment:** {generate_sentiment()}")
    #         st.markdown(f"**Priority:** {generate_priority()}")
    #         if st.button("Show Thread Summary", key=f"btn_summary_{index}"):
    #             # Display a modal with the email thread
    #             st.modal(title="Email Thread Summary", content=f"Inbound: {row['Body']}\n\nResponse: {generate_response(row['Body'])}")
    #         if st.button("Reply", key=f"btn_reply_{index}"):
    #             # Go to a new page with the inbound email and a form field with a suggested response
    #             st.session_state['current_email'] = row['Body']
    #             st.rerun()
    # Display labels outside the expander for immediate visibility
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            st.write(f"From: {row['From']}")
            st.write(f"Subject: {row['Subject']}")
        with col2:
            st.markdown(f"**Category:** Support")
        with col3:
            st.markdown(f"**Sentiment:** {generate_sentiment()}")
            st.markdown(f"**Priority:** {generate_priority()}")

        
        # Now the expander just for the email body
        with st.expander("Show Email Thread"):
            st.write(f"Inbound Email: {row['Inbound_Body']}")
            st.write(f"Reply: {row['Reply_Body']}")

            #####################################################################
            # Thread summarizer
            # Initialize a unique key for the thread summary state
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
                    summary = generate_thread_summary(row['Inbound_Body'], row['Reply_Body'])
                    st.write(summary)

            #####################################################################
            # Reply form        
            
            if st.button("Generate Reply", key=f"btn_reply_{index}"):
                # Go to a new page with the inbound email and a form field with a suggested response
                st.session_state['current_email'] = row['Inbound_Body']
                st.session_state['show_inbox'] = False
                st.rerun()


# Simulated function to generate a thread summary that takes some time
def generate_thread_summary(inbound_body, reply_body):
    # Simulate a time-consuming process
    import time
    time.sleep(2)  # replace this with the actual logic
    return f"Inbound: {inbound_body}\n\nResponse: {reply_body}"

# Display the email reply page
def display_reply_page():
    st.write(st.session_state['current_email'])
    suggested_response = generate_response(st.session_state['current_email'])
    response = st.text_area("Your Response", value=suggested_response)

    if st.button("Send Response"):
        st.success("Response sent!")

    # Back button to return to the inbox
    if st.button("Back to Inbox"):
        st.session_state['show_inbox'] = True
        st.rerun()


st.title("Inbox")
csv_file_path = 'new_corrected_support_emails.csv'  # Replace with your CSV file path
df = load_data(csv_file_path)

# Initialize the session state for page control
if 'show_inbox' not in st.session_state:
    st.session_state['show_inbox'] = True  # Show inbox by default

if st.session_state['show_inbox']:
    display_inbox(df)
else:
    display_reply_page()    


