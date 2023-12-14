from flask import Flask, request, jsonify
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

BTC_WEBHOOK_URL = "https://discord.com/api/webhooks/1166011593398685866/0kWVhUMu2WM1VoQQH6yD5WaUrp817GdTmaVUqEbLwIc53YrM04XWkiQcfK6sLy84rt4H"
ETH_WEBHOOK_URL = "https://discord.com/api/webhooks/1166011674722046022/KuVIIznYZEA-EdMxnbSC6m6QmoUkN_oiGMF4T7MA7JMa-xzRNZRbYC-UjNc5i2rOUsjp"
GEN_WEBHOOK_URL = "https://discord.com/api/webhooks/1167431874084347934/PvzyBtL7e3QGwwtwydW3QqVYFnOoIHYyGhoCTMU8bSC8JBRFJBaVR5M1_-anipqgyir1"
BNB_WEBHOOK_URL = "https://discord.com/api/webhooks/1173209498249330748/tUGRgPbn3PHNO-Brvuu4IemrzwVGg895jj8ZD21j0v-VIx7SNm92L6cnwHxFApbBD3el"
AVAX_WEBHOOK_URL = "https://discord.com/api/webhooks/1173209704269357116/fR5kWwo6xYZLBajA2JuGsJMIXZjkVk-uwBybMdkPPOMXUC9Mo58eGpM3DQ6yTH5CECla"
SOL_WEBHOOK_URL = "https://discord.com/api/webhooks/1173209824692019300/dD37jmai9ZNGKK6v2XZyjEJb8gtmFiQq_EcM2uDDKoDFl5bELWOIuwUvZPm7VUR2TXHP"

TECH_STOCKS_WEBHOOK_URL = "https://discord.com/api/webhooks/1172763762172895242/aiED4ExnVk-Bn-iXnWDLq2gqrL18mv1csxsvciGrQvZa6OHcd2B1jH_CcaKn73r_nE5t"
SP_500_WEBHOOK_URL = "https://discord.com/api/webhooks/1172763639560806400/mPF8-dClxKWWP9nhfrWB2EJoTrGAJYgVQeNAP4Hm5I202reXgkDUiXUS-wBQ5KJt6--N"

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


Crypto = ['ETHUSDT', 'BTCUSDT', 'SOL', 'AVAX', 'BNB']
Stocks = ['SP500', 'AAPL', 'AMZN', 'TSLA', 'MSFT']

# Different Chats
    # English language IDs
eng_crypto = -1002061730936
eng_stocks = -1002069223522


def send_telegram_message(embed):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

        
        
    if str(embed['title'].split(' ')[2]) in Crypto:
        chat_id = str(eng_crypto)
        print(chat_id)
    elif str(embed['title'].split(' ')[2]) in Stocks:
        chat_id = str(eng_stocks)
    print(chat_id)
    # Convert UTC time to human-readable time


    message_text = f"<b>{embed['title']}</b>\n\n"
    message_text += f"Description: {embed['description']}\n"
    message_text += f"Exchange: {embed['Exchange']}\n"
    message_text += f"Value: {embed['value']}\n"

    message_text += f"Chart: https://www.tradingview.com/chart/FmkMFm8K/?symbol=SP%3ASPX\n\n"

    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'HTML'
    }

    requests.post(url, json=payload)
    
def send_discord_message(embed, url):
    
    color = 16711680
    conviction = embed.get('conviction', 'Default Condition')
    first_word = conviction.split()[1]
    if first_word == 'SHORT':
        color = 16711680
    else:
        color = 65280
    
    # payload = {"embeds": [embed]}
    # payload['title'] = embed.get('condition', 'Default Condition')
    # payload['description'] = "Description"
    # payload['color'] = 16711680,
    # payload['footer'] = {"text": "Footer Text"},
    timestamp_string = embed.get('Time', 'Default Condition')
# Remove the trailing " UTC"
    timestamp_string = timestamp_string.replace(' UTC', '')
    parsed_timestamp = datetime.strptime(timestamp_string, '%Y-%m-%dT%H:%M:%S%z')
    embed2 = {
    "title": embed.get('conviction', 'Default Condition'),
    "description": "",
    "color": color,  # Red color
    "fields": [
        {"name": "Exchange", "value": embed.get('Exchange', 'Default Condition'), "inline": True},
        {"name": "Price", "value": embed.get('value', 'Default Condition'), "inline": True}
    ],
    "footer": {"text": "Footer Text"},
    
    "timestamp": parsed_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')

}
    embed = {
    "title": "Embed Title",
    "description": "Embed Description",
    "color": 16711680,  # Red color
    "fields": [
        {"name": "Field 1", "value": "Value 1", "inline": True},
        {"name": "Field 2", "value": "Value 2", "inline": True}
    ],
    "footer": {"text": "Footer Text"},
    "timestamp": "2023-10-26T10:00:00Z"
}
    
    payload = {"embeds": [embed2]}
    print(payload)

    requests.post(url, json=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)
    
    url = ""

    embed_data = {
        'title': data.get('conviction', 'Default Condition'),
        'description': 'Embed Description',
        'color': 16711680,
        'value': data.get('value'),
        'Exchange': data.get('Exchange', 'Default Condition'),

    }

    if str(embed_data['title'].split(' ')[2]) == "ETHUSDT":
        url = ETH_WEBHOOK_URL
    elif str(embed_data['title'].split(' ')[2]) == "BTCUSDT":
        url = BTC_WEBHOOK_URL
    elif str(embed_data['title'].split(' ')[2]) == "SOL":
        url = SOL_WEBHOOK_URL
    elif str(embed_data['title'].split(' ')[2]) == "AVAX":
        url = AVAX_WEBHOOK_URL
    elif str(embed_data['title'].split(' ')[2]) == "BNB":
        url = BNB_WEBHOOK_URL
    elif str(embed_data['title'].split(' ')[2]) == "SP500":
        url = SP_500_WEBHOOK_URL
        
    elif str(embed_data['title'].split(' ')[2]) == "AAPL" or str(embed_data['title'].split(' ')[2]) == "AMZN" or str(embed_data['title'].split(' ')[2]) == "TSLA" or tr(embed_data['title'].split(' ')[2]) == "MSFT":
        url = TECH_STOCKS_WEBHOOK_URL
        


    send_telegram_message(embed_data)
    send_discord_message(data, url)
    send_discord_message(data, GEN_WEBHOOK_URL)
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(port=8000)
