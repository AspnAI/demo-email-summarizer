import requests
from bs4 import BeautifulSoup

def getWebsiteText(url='https://www.example.com'):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    return text.replace("\n"," ")
