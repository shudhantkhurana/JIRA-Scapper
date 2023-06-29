from flask import Flask, render_template, request
from flask_mail import Mail, Message
import requests
import mailConfig
import logging.config
logging.config.fileConfig('logging.conf')

local_server = True
app = Flask(__name__)
mailConfig.app_config(app)
mail = Mail(app)

@app.route('/', methods=["GET"])
def index():
    
    msg = Message(
                    'Test',
                    sender ='demo.shudhant@gmail.com',
                    recipients = ['shudhant007@gmail.com']
                    )
    msg.body = 'Hello Flask message Test'
    mail.send(msg)
    return 'Sent'

if __name__ == '__main__':
    if local_server:
        app.run( debug=True)
        response = requests.get('https://127.0.0.1:5000')
        if response.status_code == 200:
            logging.info(response.text)
        else:
            logging.error(response.status_code)
            