from langchain.output_parsers import ResponseSchema

# these are the parameters for the LLM Chain
class GptParameters:
    MODEL_NAME: str = "gpt-4"
    TEMPERATURE: float = 0


# this is the response schema for the LLM Response in JSON format. If you modify it, you need to adjust the code in tools/generateEmails.py
class GptResponse:
    RESPONSE_SCHEMA: list = [
        ResponseSchema(name='To', description='Insert Recipient email here'),
        ResponseSchema(name='From', description='Insert Sender email here'),
        ResponseSchema(name='Subject', description='Generated fake Subject'),
        ResponseSchema(name='email', description='Generated fake email'),
        ResponseSchema(name='priority', description='Generated fake priority'),
        ResponseSchema(name='category', description='Generated fake category'),
        ResponseSchema(name='sentiment', description='Generated fake sentiment'),
    ]


class PieChatParameters:
    BACKGROUND_COLOR: str = '#0e1117'
    TITLE_COLOR: str = 'white'
    TITLE_FONT_SIZE: int = 16
    TITLE_FONT_WEIGHT: str = 'bold'
    TITLE_PAD: int = 20
    TEXT_COLOR: str = 'white'

class EmailGenerationParameters:
    SUPPORT_EMAILS: int = 5
    SALES_EMAILS: int = 3
    SPAM_EMAILS: int = 1
    NOTIFICATION_EMAILS: int = 1