# demo-email-summarizer

## Installation ##
Refer to main branch README.md

## Important Note 
You need to add your OpenAI API key to as your ENV variable.
``` OPENAI_API_KEY=YOUR_API_KEY```

## To change Model Parameters, Pie Chart settings, Email Count and Response Schema ##
Go to `tools/variables.py` and adjust the parameters according to your needs.

## To Change Prompts
Go to `tools/prompts/templates.py` and adjust the prompts according to your needs.

## Info About Files
- `Home.py` is the main file that runs the streamlit app.
- `tools/variables.py` contains all the variables that can be adjusted to change the model parameters, pie chart settings, email count and response schema.
- `tools/prompts/templates.py` contains all the prompts that can be adjusted to change the prompts.
- `tools/openai.py` contains the OpenAI API call functions.
- `company_info.txt` contains the company information that is generated by the Model.
- `support.txt` contains the fake support email that is generated by the Model.
- `pages` contains all the pages that are used in the streamlit app.