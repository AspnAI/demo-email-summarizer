import os
from dotenv import load_dotenv
load_dotenv()

# Chat and converse
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.chains import ConversationChain

# Summarizer
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.document import Document


openAIModel='gpt-4-1106-preview'

chat = ChatOpenAI(model=openAIModel)

def summarizeEmailThread(emailThread):
    prompt_template = """Write a concise summary of the following email thread:
    "{text}"
    CONCISE SUMMARY:"""
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name=openAIModel)
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = [Document(page_content=x) for x in text_splitter.split_text(emailThread)]

    return(stuff_chain.run(docs))




def getAIResponse(systemPrompt,query):
    chat_completion = chat([
        SystemMessage(content=systemPrompt),
        HumanMessage(content=query)
    ])

    return chat_completion.content


class Converse:
    def __init__(self):
        self.conversation = ConversationChain(llm=chat)

    def getAIResponse(self,query):
        return self.conversation.run(query);
