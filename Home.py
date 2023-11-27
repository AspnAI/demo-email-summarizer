from tools import openai
from tools import scraper
import streamlit as st
import pandas as pd
import random
from streamlit_modal import Modal
import streamlit.components.v1 as components
import streamlit_scrollable_textbox as stx
import os
from langchain.schema.document import Document
from langchain.chains import ReduceDocumentsChain, MapReduceDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from tools import generateEmails
from tools import variables
from tools.prompts.templates import TemplatesOfPrompts
from PIL import Image




def generateSummaryOfCompany(company_info):
    prompt_template = TemplatesOfPrompts.PROMPT_TEMPLATE_FOR_COMPANY_DESCRIPTION
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm = ChatOpenAI(
        temperature=variables.GptParameters.TEMPERATURE, 
        model_name=variables.GptParameters.MODEL_NAME
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain, 
        document_variable_name="doc_summaries"
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, 
        chunk_overlap=100
    )
    docs = [
        Document(page_content=x) for x in text_splitter.split_text(company_info)
    ]

    return(stuff_chain.run(docs))

def generateSupportEmailForCompany(company_info):
    print("Generating Support Email")
    support_email = openai.getAIResponse(
        "Generate a fake support email address for the company keeping in mind the information provided to you. For example like support@abc.com etc. Return only email address, not anything else. Example: support@abc.com",
        f"Company Information: {company_info}\
    ")
    # save email in support.txt
    with open("support.txt", "w") as f:
        f.write(support_email)
    return support_email


image = Image.open('assets/aspn-white.png')

def main():
    st.set_page_config(
        page_title="Récapitulateur d'e-mails", 
        page_icon=image, 
        initial_sidebar_state="auto"
    )
    st.image(image, width=200)
    st.title("Email Summarizer")
    # st.markdown("**SUMMARIZE YOUR EMAILS WITH EASE**")

    st.divider()

    st.subheader("Veuillez saisir l'URL du site Web de votre entreprise")
    
    website_url = st.text_input(
        "Entrez l'URL du site:", value="", max_chars=None, key=None, type="default",
        help=None, autocomplete=None, on_change=None, args=None, kwargs=None,
        placeholder="https://www.example.com", disabled=False, label_visibility="visible"
    )

    scrape_button = st.button(
        "Collecter des informations", key=None, help=None, on_click=None,
        args=website_url, kwargs=None, type="primary", disabled=False, 
        use_container_width=False
    )

    if scrape_button:
        try:
            with st.spinner("Le système collecte des informations..."):
                website_text = scraper.getWebsiteText(website_url)
                st.session_state['website_text'] = website_text
        except:
            st.write("Veuillez saisir une URL valide")
        st.subheader("Opération")
        with st.spinner("Le système analyse les informations..."):
            company_info = generateSummaryOfCompany(website_text)
            # save company info in company_info.txt
            with open("company_info.txt", "w") as f:
                f.write(company_info)
            st.session_state['company_info'] = company_info
            support_email = generateSupportEmailForCompany(
                st.session_state['company_info']
            )
            st.session_state['support_email'] = support_email
        st.markdown(":white_check_mark: Votre profil est complet.")

        # now we will generate 10 fake emails for the company
        st.subheader("Générer des exemples d'e-mails")
        with st.spinner("Générer des exemples d'e-mails..."):
            generateEmails.generateFakeEmails(company_info, support_email)
        st.markdown(":white_check_mark: Exemples d'e-mails générés")
        st.divider()   

        st.write("**Vous pouvez désormais utiliser la barre latérale pour accéder aux pages de la boîte de réception et des statistiques.**")

        # goToInbox = st.button("Go to Inbox", key=None, help=None, on_click=None,
        #                     args=None, kwargs=None, type="primary", disabled=False, use_container_width=False)
        # goToStats = st.button("Go to Statistics", key=None, help=None, on_click=None,
        #                     args=None, kwargs=None, type="secondary", disabled=False, use_container_width=False)
        # if goToInbox:
        #     st.session_state['show_inbox'] = True
        # if goToStats:
        #     st.session_state['show_stats'] = True

if __name__ == "__main__":
    main()
