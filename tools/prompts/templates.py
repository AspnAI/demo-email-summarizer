class TemplatesOfPrompts:
    PROMPT_TEMPLATE_FOR_COMPANY_DESCRIPTION: str = """
    As an expert in generating detailed and accurate technical descriptions, provide a brief but specific and technically-oriented description of a company's contributions and activities based on the provided summaries extracted from their company website in French.

    ### INSTRUCTIONS ###

    Read the set of summaries extracted from the company website {doc_summaries}, and using your technical expertise, provide a comprehensive description of the company's specific contributions and activities in French. Focus on the following aspects:

    1. Specialization: Describe the company's area of expertise within the industry, highlighting any unique technologies, products, or services they offer.

    2. Technical Details: Provide specific technical information about the company's products or services. Include details on functionality, design features, and any innovations that set them apart in the industry.

    3. Industry Impact: Discuss the company's overall contributions and impact within the space industry. Highlight significant projects, collaborations, or advancements that have propelled their reputation.

    Your description should aim to be both detailed and accurate, ensuring a comprehensive understanding of the company.
    Keep your description in French and within 100-125 words.
    Return only summary, not anything else.
    Helpful Answer:
    """


    PROMPT_TEMPLATE_FOR_REPLY: str = '''
        ### Instructions
        Your goal is to generate only one fake reply email for a email. You will be given a company description that briefly describes what company workings. Here is the company description: {company_info}
        Here is the email body you've to reply: {email}
        User Email: {user_email}
        Sentiment: {sentiment}
        Priority: {priority}
        Category: {category}

        1- Mention user if user is mentioned in the email.
        2- Keep sentiment same as email.
        3- Keep user email same and keep your email same. Here is the email you have to use for company: {company_email}
        4- Add Re: in the subject.
        5- Make the reply in the French.

        Follow this format for the output: {format_instructions}
        Helpful Answer:
        '''

    PROMPT_TEMPLATE_FOR_NOTIFICATION_EMAIL: str = """
        Here is what you've generated so far: {email_list}

        ### Instructions
        Your goal is to generate only one fake Notification inbound email for a company. You will be given a company description that briefly describes what company workings. Here is the company description:
        {company_info}
        Here are the steps you must perform to generate the fake emails:
        1- Write a fake email that is similar to the emails that the company receives on a daily basis.
        2- Use company email address as recipient email address. {company_email}
        3- Generate fake sender email address based like juliaburke@gmail.com, cherrysheila@hotmail.com, frances43@young-bradford.com etc
        4- Generate fake subject like "Need help with your product", "Need help with your service", "Need help with your software", etc.
        5- USe fake names like John Doe, Jane Doe, etc.
        6- Also pick fake priorities from this list ["High", "Medium", "Low"]
        8- Also pick Sentiment from this list ["Positive", "Negative", "Neutral"]
        7- Category: Notification
        8- Make this email in French

        Follow this format for the output: {format_instructions}
        Helpful Answer:
        """

    PROMPT_TEMPLATE_FOR_SPAM_EMAIL: str = """
        Here is what you've generated so far: {email_list}

        ### Instructions
        Your goal is to generate only one fake Spam inbound email for a company. You will be given a company description that briefly describes what company workings. Here is the company description:
        {company_info}
        Here are the steps you must perform to generate the fake emails:
        1- Write a fake email that is similar to the emails that the company receives on a daily basis.
        2- Use company email address as recipient email address. {company_email}
        3- Generate fake sender email address based like juliaburke@gmail.com, cherrysheila@hotmail.com, frances43@young-bradford.com etc
        4- Generate fake subject like "Need help with your product", "Need help with your service", "Need help with your software", etc.
        5- USe fake names like John Doe, Jane Doe, etc.
        6- Also pick fake priorities from this list ["High", "Medium", "Low"]
        7- Also pick Sentiment from this list ["Positive", "Negative", "Neutral"]
        8- Category: Spam
        9- Make this email in French

        Follow this format for the output: {format_instructions}
        Helpful Answer:
        """

    PROMPT_TEMPLATE_FOR_SALES_EMAIL:str = """
        Here is what you've generated so far: {email_list}

        ### Instructions
        Your goal is to generate only one fake Sales inbound email for a company. You will be given a company description that briefly describes what company workings. Here is the company description:
        {company_info}
        Here are the steps you must perform to generate the fake emails:
        1- Write a fake email that is similar to the emails that the company receives on a daily basis.
        2- Use company email address as recipient email address. {company_email}
        3- Generate fake sender email address based like juliaburke@gmail.com, cherrysheila@hotmail.com, frances43@young-bradford.com etc
        4- Generate fake subject like "Need help with your product", "Need help with your service", "Need help with your software", etc.
        5- Use fake names like John Doe, Jane Doe, etc.
        6- Also pick fake priorities from this list ["High", "Medium", "Low"]
        7- Also pick Sentiment from this list ["Positive", "Negative", "Neutral"]
        8- Category: Sales
        9- Make this email in French

        Follow this format for the output: {format_instructions}
        Helpful Answer:
        """

    PROMPT_TEMPLATE_FOR_SUPPORT_EMAIL = """
        Here is what you've generated so far: {email_list}

        ### Instructions
        Your goal is to generate only one fake Support inbound email for a company. You will be given a company description that briefly describes what company workings. Here is the company description:
        {company_info}
        
        Here are the steps you must perform to generate the fake emails:
        1- Write a fake email that is similar to the emails that the company receives on a daily basis.
        2- Use company email address as recipient email address. {company_email}
        3- Generate fake sender email address based like juliaburke@gmail.com, cherrysheila@hotmail.com, frances43@young-bradford.com etc
        4- Generate fake subject like "Need help with your product", "Need help with your service", "Need help with your software", etc.
        5- USe fake names like John Doe, Jane Doe, etc.
        6- Also pick fake priorities from this list ["High", "Medium", "Low"]
        7- Category: Support
        8- Also pick Sentiment from this list ["Positive", "Negative", "Neutral"]
        9- Make this email in French

        Follow this format for the output: {format_instructions}
        Helpful Answer:
        """