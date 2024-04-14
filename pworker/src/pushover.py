import requests
import os 

PUSHOVER_TOKEN =  os.environ.get('PUSHOVER_TOKEN')
PUSHOVER_USER =  os.environ.get('PUSHOVER_USER')

def send_pushover_notification(message):
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": PUSHOVER_TOKEN,
        "user": PUSHOVER_USER,
        "message": message,
        "priority": 1
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        return "Message sent successfully."
    else:
        return f"Error sending message. Status code: {response.status_code}"
