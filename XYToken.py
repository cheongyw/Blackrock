import telepot
import json 
import requests
import time
import urllib
from bs4 import BeautifulSoup
import json
from pprint import pprint

token='392920506:AAHPmmPeCuqFSBdqf5cswmN2Ew9oj-ZLUtg'
URL = "https://api.telegram.org/bot{}/".format(token)
TelegramBot=telepot.Bot(token)
chat=171391200

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content
	
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js
	
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)
		
def send_message(text, chat):
	text = urllib.parse.quote_plus(text)
	url = URL + "sendMessage?text={}&chat_id={}".format(text, chat)
	get_url(url)


# Returns the performance for the sixth month
def sixthMonthReturn():
	perf_file = urllib.request.urlopen("https://www.blackrock.com/tools/hackathon/performance?&identifiers=ticker%3AIVV&graph=resultMap.RETURNS.latestPerf")
	data = json.loads(perf_file.read().decode('utf-8'))
	perf_file.close()
	return str(data["resultMap"]["RETURNS"][0]["latestPerf"]["sixMonth"])
	
#text, chat = get_last_chat_id_and_text(get_updates())
#send_message(text, chat)

#Sends First message

def main():
	initialText="Please enter the relevant details."
	last_textchat=(None,None)
	while True:
		text, chat = get_last_chat_id_and_text(get_updates())
		if (text, chat) != initialText:
			send_message(sixthMonthReturn,chat)

if __name__ == '__main__':
	main()
	