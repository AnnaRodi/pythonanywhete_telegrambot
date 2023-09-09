#!/usr/bin/python3.6
from flask import Flask, request
import telepot
import urllib3

#lesson https://blog.pythonanywhere.com/148/

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = "8279db9c-738a-4891-ab3e-617c13b40770"  #сгенерированно здесь https://www.guidgenerator.com/online-guid-generator.aspx
bot = telepot.Bot('6201217395:AAEGTPOsK_tq15RQPmMsNDvGdJdJaobvcIE')
bot.setWebhook("https://experta.pythonanywhere.com/{}".format(secret), max_connections=1)

app = Flask(__name__)

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        if "text" in update["message"]:
            text = update["message"]["text"]
            bot.sendMessage(chat_id, "From the web: you said '{}'".format(text))
            bot.sendMessage(chat_id, "From the web: you said '{}'".format(update["message"]))
        else:
            bot.sendMessage(chat_id, "From the web: sorry, I didn't understand that kind of message")
    return "OK"
