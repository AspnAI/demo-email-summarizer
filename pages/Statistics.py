import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from tools import variables
import os


def load_data(csv_file):
    df = pd.read_csv(csv_file)
    print(f"Loadeding data on Statistics page")
    # remove replies emails
    if 'support_email' in st.session_state:
        df = df[df['To'] == st.session_state['support_email']]
    else:
        with open("support.txt", "r") as f:
            support_email = f.read()
            df = df[df['To'] == support_email]
    # remove whitespaces and convert to lowercase
    df['To'] = df['To'].str.strip().str.lower()
    return df



def calculate_distribution(df, column_name):
    return df[column_name].value_counts(normalize=True)


def create_pie_chart(data, title):
    fig, ax = plt.subplots()
    ax.pie(data, labels=data.index, explode=[0.09]*len(data),
        autopct='%1.1f%%', startangle=90,
        textprops={'color': variables.PieChatParameters.TEXT_COLOR})
    ax.axis('equal')
    plt.title(title, 
            color=variables.PieChatParameters.TITLE_COLOR, 
            fontsize=variables.PieChatParameters.TITLE_FONT_SIZE,
            fontweight=variables.PieChatParameters.TITLE_FONT_WEIGHT,
            pad=variables.PieChatParameters.TITLE_PAD,
        )
    fig.patch.set_facecolor(variables.PieChatParameters.BACKGROUND_COLOR)  # Set the background color
    return fig


def showStats(load_data, calculate_distribution, create_pie_chart):
    st.title("Email Analysis Dashboard")
    csv_file_path = 'emails_data.csv'  # Replace with the path to your CSV file
    if os.path.exists(csv_file_path) == False:
        st.warning("Please set the CSV file path in the code.")
    else:
        df = load_data(csv_file_path)
        tab1, tab2, tab3, tab4 = st.tabs(["Category", "Sentiment", "Priority", "Company"])
        # Category Pie Chart in the first tab
        with tab1:
            st.subheader("Email Category Distribution")
            category_distribution = calculate_distribution(df, 'Category')
            st.pyplot(create_pie_chart(category_distribution, "Category"))

        # Sentiment Pie Chart in the second tab
        with tab2:
            st.subheader("Email Sentiment Distribution")
            sentiment_distribution = calculate_distribution(df, 'Sentiment')
            st.pyplot(create_pie_chart(sentiment_distribution, "Sentiment"))

        # Priority Pie Chart in the third tab
        with tab3:
            st.subheader("Email Priority Distribution")
            priority_distribution = calculate_distribution(df, 'Priority')
            st.pyplot(create_pie_chart(priority_distribution, "Priority"))

        with tab4:
            st.subheader("Company Information")
            if 'company_info' not in st.session_state:
                with open("company_info.txt", "r") as f:
                    company_info = f.read()
                    st.write(f"{company_info}")
            else:
                st.write(f"{st.session_state['company_info']}")

showStats(load_data, calculate_distribution, create_pie_chart)