from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from pprint import pprint
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import csv
import streamlit as st
from tools import variables
from tools.prompts.templates import TemplatesOfPrompts
import concurrent.futures

outputParser = StructuredOutputParser.from_response_schemas(
    variables.GptResponse.RESPONSE_SCHEMA)
format_instructions = outputParser.get_format_instructions()
data = []


def generateSupportEmails(format_instructions):
    prompt_template = TemplatesOfPrompts.PROMPT_TEMPLATE_FOR_SUPPORT_EMAIL
    prompt = PromptTemplate.from_template(
        template=prompt_template, 
        partial_variables={"format_instructions": format_instructions}
    )
    llm = ChatOpenAI(
        temperature=variables.GptParameters.TEMPERATURE, 
        model=variables.GptParameters.MODEL_NAME
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain


def generateSalesEmails(format_instructions):
    prompt_template = TemplatesOfPrompts.PROMPT_TEMPLATE_FOR_SALES_EMAIL
    prompt = PromptTemplate.from_template(
        template=prompt_template, 
        partial_variables={ "format_instructions": format_instructions}
    )
    llm = ChatOpenAI(
        temperature=variables.GptParameters.TEMPERATURE, 
        model=variables.GptParameters.MODEL_NAME
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain


def generateSpamEmails(format_instructions):
    prompt_template = TemplatesOfPrompts.PROMPT_TEMPLATE_FOR_SPAM_EMAIL
    prompt = PromptTemplate.from_template(
        template=prompt_template, 
        partial_variables={"format_instructions": format_instructions}
    )
    llm = ChatOpenAI(
        temperature=variables.GptParameters.TEMPERATURE, 
        model=variables.GptParameters.MODEL_NAME
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain


def generateNotificationEmails(format_instructions):
    prompt_template = TemplatesOfPrompts.PROMPT_TEMPLATE_FOR_NOTIFICATION_EMAIL
    prompt = PromptTemplate.from_template(
        template=prompt_template, 
        partial_variables={"format_instructions": format_instructions}
    )
    llm = ChatOpenAI(
        temperature=variables.GptParameters.TEMPERATURE, 
        model=variables.GptParameters.MODEL_NAME
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain


def saveDataToCSV(data):
    with open('emails_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["To", "From", "Subject", "Body",
                        "Priority", "Category", "Sentiment"])
        for i in data:
            writer.writerow([i['To'], i['From'], i['Subject'], i['email'],
                            i['priority'], i['category'], i['sentiment']])


def generate_and_parse_email(email_generator, count, company_info, support_email, email_list):
    emails = []
    for i in range(count):
        email = email_generator(format_instructions=format_instructions).run(
            company_info=company_info, 
            email_list=email_list, 
            company_email=support_email
        )
        parsedEmail = outputParser.parse(email)
        emails.append(parsedEmail)
    return emails


def generateFakeReply(format_instructions):
    prompt_template = TemplatesOfPrompts.PROMPT_TEMPLATE_FOR_REPLY
    prompt = PromptTemplate.from_template(
        template=prompt_template, 
        partial_variables={"format_instructions": format_instructions}
    )
    llm = ChatOpenAI(
        temperature=variables.GptParameters.TEMPERATURE,
        model=variables.GptParameters.MODEL_NAME
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain


def generateFakeReplyEmails(email, company_info, support_email):
    reply_emails = generateFakeReply(format_instructions=format_instructions).run(
        company_info=company_info, email=email['email'],
        user_email=email['From'], sentiment=email['sentiment'],
        priority=email['priority'], category=email['category'],
        company_email=support_email)
    parsedEmail = outputParser.parse(reply_emails)
    return parsedEmail


# def generateFakeEmails(company_info, support_email):
#     support_emails = []
#     for i in range(variables.EmailGenerationParameters.SUPPORT_EMAILS):
#         support_emails.append(generateSupportEmails(format_instructions=format_instructions).run(
#             company_info=company_info, email_list=support_emails, company_email=support_email))
#         parsedEmail = outputParser.parse(support_emails[i])
#         data.append(parsedEmail)

#     pprint('--- Support Emails Done ---')


#     sales_emails = []
#     for i in range(variables.EmailGenerationParameters.SALES_EMAILS):
#         sales_emails.append(generateSalesEmails(format_instructions=format_instructions).run(
#             company_info=company_info, email_list=sales_emails, company_email=support_email))
#         parsedEmail = outputParser.parse(sales_emails[i])
#         data.append(parsedEmail)

#     pprint('--- Sales Emails Done ---')


#     spam_emails = []
#     for i in range(variables.EmailGenerationParameters.SPAM_EMAILS):
#         spam_emails.append(generateSpamEmails(format_instructions=format_instructions).run(
#             company_info=company_info, email_list=spam_emails, company_email=support_email))
#         parsedEmail = outputParser.parse(spam_emails[i])
#         data.append(parsedEmail)

#     pprint('--- Spam Emails Done ---')

#     # generate one email for notification
#     notification_emails = []
#     for i in range(variables.EmailGenerationParameters.NOTIFICATION_EMAILS):
#         notification_emails.append(generateNotificationEmails(format_instructions=format_instructions).run(
#             company_info=company_info, email_list=notification_emails, company_email=support_email))
#         parsedEmail = outputParser.parse(notification_emails[i])
#         data.append(parsedEmail)

#     pprint('--- Notification Emails Done ---')

#     # here we will generate fake replies for each email
#     new_data = []
#     for i in range(len(data)):
#         pprint(f"--- Generating Reply for index {i} ---")
#         new_data.append(generateFakeReplyEmails(
#             data[i], company_info, support_email))

#     for i in range(len(new_data)):
#         data.append(new_data[i])

#     for i in range(int((len(data) / 2))):
#         data[i]['To'] = support_email

#     for i in range((int(len(data) / 2)) + 1, len(data)):
#         data[i]['From'] = support_email
#     saveDataToCSV(data)

def generateFakeEmails(company_info, support_email):
    data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_email_type = {
            executor.submit(generate_and_parse_email, generateSupportEmails, variables.EmailGenerationParameters.SUPPORT_EMAILS, company_info, support_email, []): 'support',
            executor.submit(generate_and_parse_email, generateSalesEmails, variables.EmailGenerationParameters.SALES_EMAILS, company_info, support_email, []): 'sales',
            executor.submit(generate_and_parse_email, generateSpamEmails, variables.EmailGenerationParameters.SPAM_EMAILS, company_info, support_email, []): 'spam',
            executor.submit(generate_and_parse_email, generateNotificationEmails, variables.EmailGenerationParameters.NOTIFICATION_EMAILS, company_info, support_email, []): 'notification'
        }

        for future in concurrent.futures.as_completed(future_to_email_type):
            email_type = future_to_email_type[future]
            try:
                emails = future.result()
                data.extend(emails)
                pprint(f'--- {email_type.capitalize()} Emails Done ---')
            except Exception as exc:
                print(
                    f'{email_type.capitalize()} email generation generated an exception: {exc}')

    # Generating fake replies in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_reply = {executor.submit(
            generateFakeReplyEmails, email, company_info, support_email): email for email in data}

        for future in concurrent.futures.as_completed(future_to_reply):
            email = future_to_reply[future]
            try:
                reply = future.result()
                data.append(reply)
                pprint(f'--- Generating Reply for {email["Subject"]} ---')
            except Exception as exc:
                print(
                    f'Reply generation for {email["Subject"]} generated an exception: {exc}')

    # Processing the data
    for i in range(int((len(data) / 2))):
        data[i]['To'] = support_email

    for i in range((int(len(data) / 2)) + 1, len(data)):
        data[i]['From'] = support_email

    saveDataToCSV(data)
