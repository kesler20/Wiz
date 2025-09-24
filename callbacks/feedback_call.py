import datetime
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import smtplib
from email.message import EmailMessage
import base64
from app import app, cache

##==========================================
## Record responses from input form and send email
##===========================================
@app.callback(
    [
        Output('feedback-fname','value'),
        Output('feedback-lname','value'),
        Output('feedback-email','value'),
        Output('feedback-radio','value'),
    ],
    [
        Input('feedback-submit','n_clicks')
    ],
    [
        State('feedback-fname','value'),
        State('feedback-lname','value'),
        State('feedback-email','value'),
        State('feedback-radio','value'),
        State('feedback-text','value')
    ],
    prevent_initial_call = True
)
def email_password(n_clicks,first_name, last_name, email, radio, message):
    # Process radio button value
    if radio == 1:
        radio = 'BUG'
    elif radio == 2:
        radio = 'USAGE'
    elif radio == 3:
        radio = 'SUGGESTION'
    else:
        radio = 'OTHER'
    
    if first_name is None:
        return '','','',1

    # Email the message
    receivers = ['p.moghadam@ucl.ac.uk', 'wizapp4.0@gmail.com']
    # receivers = ['YOUR EMAIL HERE'] # for testing
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('wizapp4.0', "wizapp2023")

    # Send message to Peyman
    msg = EmailMessage()
    msg.set_content(' Hi Peyman,\n\nA Wiz user wants to contact you.\n\nName: ' + first_name + ' ' +
        last_name + '\nEmail: ' + email + '\nMessage:\n' + message + '\n\nBest,\nWiz Bot')
    msg['Subject'] = 'Wiz Feedback [' + radio + ']'
    msg['From'] = 'Wiz <wizapp4.0@gmail.com>'
    msg['To'] = receivers

    server.send_message(msg)
    server.quit()

    return '','','',1
