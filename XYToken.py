import telepot
import json
import requests
import time
import urllib
import json
from pprint import pprint
import csv


#BARRICK GOLD CORP, APPLE INC

token = '392920506:AAHPmmPeCuqFSBdqf5cswmN2Ew9oj-ZLUtg'
URL = "https://api.telegram.org/bot{}/".format(token)
TelegramBot = telepot.Bot(token)
chat = 171391200

dict = {}

with open('security-universe_20171014.csv', newline='', encoding='utf-8') as csvfile:
    securityList = csv.reader(csvfile, delimiter=',', quotechar='|')
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
    last_update=num_updates
    if last_update>0:
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        update_id = updates["result"][last_update]["update_id"]
    else:
        last_update=0
        text="None"
        chat_id=0
        update_id=0
    return (text, chat_id,update_id)


def send_message(text, chat):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat)
    get_url(url)

# Sends comments with the addition of the six month performance data.


def send_digitPhase1(digit, chat):
    text = " For the company listed, the six month performance is at {}. ".format(
        str(digit))
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat)
    get_url(url)


def main():
    stock,chat,update_id = get_last_chat_id_and_text(get_updates())
    update_id=update_id+1
    get_url("https://api.telegram.org/bot{}/getUpdates?offset={}".format(token,update_id))
    initialText = "Please enter the relevant details."
    errorText1 = "No performance data available."
    errorText2 = "Please enter a valid stock name."
    holder = "initial"
    while True:
        if (holder,chat,update_id) !=get_last_chat_id_and_text(get_updates()):
            stock, chat,update_id = get_last_chat_id_and_text(get_updates())
            if stock in dict:
                ticker = dict[stock]
                urlAddress = "https://www.blackrock.com/tools/hackathon/performance?&identifiers=ticker%3{}&graph=resultMap.RETURNS.latestPerf".format(
                    ticker)
                perf_file = urllib.request.urlopen(urlAddress)
                data = json.loads(perf_file.read())
                perf_file.close()
                if data["resultMap"] != {}:
                    digit = data["resultMap"]["RETURNS"][0]["latestPerf"]["sixMonth"]
                    send_digitPhase1(digit, chat)
                else:
                    send_message(errorText1, chat)
            else:
                send_message(errorText2, chat)

            holder = stock
            get_url("https://api.telegram.org/bot{}/getUpdates?offset={}".format(token,chat+1))

        else:
            send_message(initialText, chat)
            while True:
                time.sleep(1)
                if (holder, chat,update_id) != get_last_chat_id_and_text(get_updates()):
                    break


if __name__ == '__main__':
    main()
