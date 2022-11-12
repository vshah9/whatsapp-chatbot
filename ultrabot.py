import json
import requests
import datetime


class ultraChatBot():
    def __init__(self, json):
        self.json = json
        self.dict_messages = json['data']
        self.ultraAPIUrl = 'https://api.ultramsg.com/instance18514/'
        self.token = 'abt8xda3kf8oppe1'

    def send_requests(self, type, data):
        url = f"{self.ultraAPIUrl}{type}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    def send_message(self, chatID, text):
        data = {"to": chatID,
                "body": text}
        answer = self.send_requests('messages/chat', data)
        return answer

    def send_image(self, chatID):
        data = {"to": chatID,
                "image": "https://file-example.s3-accelerate.amazonaws.com/images/test.jpeg"}
        answer = self.send_requests('messages/image', data)
        return answer

    def send_video(self, chatID):
        data = {"to": chatID,
                "video": "https://file-example.s3-accelerate.amazonaws.com/video/test.mp4"}
        answer = self.send_requests('messages/video', data)
        return answer

    def send_audio(self, chatID):
        data = {"to": chatID,
                "audio": "https://file-example.s3-accelerate.amazonaws.com/audio/2.mp3"}
        answer = self.send_requests('messages/audio', data)
        return answer

    def send_voice(self, chatID):
        data = {"to": chatID,
                "audio": "https://file-example.s3-accelerate.amazonaws.com/voice/oog_example.ogg"}
        answer = self.send_requests('messages/voice', data)
        return answer

    def send_contact(self, chatID):
        data = {"to": chatID,
                "contact": "14000000001@c.us"}
        answer = self.send_requests('messages/contact', data)
        return answer

    def time(self, chatID):
        t = datetime.datetime.now()
        time = t.strftime('%Y-%m-%d %H:%M:%S')
        return self.send_message(chatID, time)

    def welcome(self, chatID, noWelcome=False):
        welcome_string = ''
        if (noWelcome == False):
            welcome_string = "Hi , welcome to WhatsApp chatbot using Python\n"
        else:
            welcome_string = """wrong command
Please type one of these commands:
*hi* : Saluting
*time* : show server time
*image* : I will send you a picture
*video* : I will send you a Video
*audio* : I will send you a audio file
*voice* : I will send you a ppt audio recording
*contact* : I will send you a contact
"""
        return self.send_message(chatID, welcome_string)

    def Processingـincomingـmessages(self):
        if self.dict_messages != []:
            message = self.dict_messages
            text = message['body'].split()
            if not message['fromMe']:
                chatID = message['from']
                if text[0].lower() == 'hi':
                    return self.welcome(chatID)
                elif text[0].lower() == 'time':
                    return self.time(chatID)
                elif text[0].lower() == 'image':
                    return self.send_image(chatID)
                elif text[0].lower() == 'video':
                    return self.send_video(chatID)
                elif text[0].lower() == 'audio':
                    return self.send_audio(chatID)
                elif text[0].lower() == 'voice':
                    return self.send_voice(chatID)
                elif text[0].lower() == 'contact':
                    return self.send_contact(chatID)
                else:
                    return self.welcome(chatID, True)
            else:
                return 'NoCommand'


import http.client
conn = http.client.HTTPSConnection("api.ultramsg.com")
payload = "token=1v941eyo9eqixrsi&to=14155552671&body=WhatsApp API on UltraMsg.com works good&priority=10&referenceId="
headers = { 'content-type': "application/x-www-form-urlencoded" }
conn.request("POST", "/instance16/messages/chat", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))