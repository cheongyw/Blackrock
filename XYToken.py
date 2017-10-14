import telepot
import json 
import requests
import time
import urllib
import json
from pprint import pprint
import csv

token='392920506:AAHPmmPeCuqFSBdqf5cswmN2Ew9oj-ZLUtg'
URL = "https://api.telegram.org/bot{}/".format(token)
TelegramBot=telepot.Bot(token)
chat=171391200

dict = {}

with open('security-universe_20171014.csv', newline='', encoding='utf-8') as csvfile:
	securityList = csv.reader(csvfile, delimiter=',',quotechar='|')
	for row in securityList:
		dict[row[1]] = row[0]

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

# Sends comments with the addition of the six month performance data.
def send_digitPhase1(digit,chat):
	text=" For the company listed, the six month performance is at {}. \n".format(str(digit))
	text=urllib.parse.quote_plus(text)
	url = URL + "sendMessage?text={}&chat_id={}".format(text, chat)
	get_url(url)

# Returns the performance for the sixth month
	
#text, chat = get_last_chat_id_and_text(get_updates())
#send_message(text, chat)

#Sends First message

def main():
	initialText="Please enter the relevant details."
	errorText="Please enter a valid stock name."
	chat=171391200
	last_textchat=(None,None)
	stock = "Initial"
	while True:
		if stock != get_last_chat_id_and_text(get_updates())[0]:
			stock, chat = get_last_chat_id_and_text(get_updates())
		 
			if stock in dict:
				ticker = dict[stock]
				urlAddress="https://www.blackrock.com/tools/hackathon/performance?&identifiers=ticker%3{}&graph=resultMap.RETURNS.latestPerf".format(ticker)
				perf_file = urllib.request.urlopen(urlAddress)
				data = json.loads(perf_file.read())
				perf_file.close()
				digit=data["resultMap"]["RETURNS"][0]["latestPerf"]["sixMonth"]
				send_digitPhase1(digit,chat)
				
			else:
				send_message(errorText,chat)
				
		else:
			send_message(initialText,chat)
			time.sleep(1)
			

if __name__ == '__main__':
	main()
	