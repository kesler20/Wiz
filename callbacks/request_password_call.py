import datetime
import dash_core_components as dcc
import dash_html_components as html
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
        Output('rp-fname','value'),
        Output('rp-lname','value'),
        Output('rp-email','value'),
        Output('rp-radio','value'),
    ],
    [
        Input('rp-submit','n_clicks')
    ],
    [
        State('rp-fname','value'),
        State('rp-lname','value'),
        State('rp-email','value'),
        State('rp-radio','value')
    ]
)
def email_password(n_clicks,first_name, last_name, email, radio):
    # Process radio button value
    if radio == 1:
        radio = 'Academia'
    elif radio == 2:
        radio = 'Industry'
    else:
        radio = 'Other'
    
    if first_name is None:
        return '','','',1
    

    # Open file to write user data
    file = open('user_data/list_of_users.txt','a+')

    # Make string to append
    user_info = first_name + ' ' + last_name + ' ' + email + ' ' + radio + ' '+ str(datetime.datetime.now())

    # Print to file in pretty way
    user_info = user_info.split()
    formated_string = '{0[0]:<15}{0[1]:<15}{0[2]:<40}{0[3]:<12}{0[4]:<12}{0[5]:<12}'.format(user_info)
    file.write(formated_string + '\n')
    file.close()

    # Email password to user
    receivers = ['p.moghadam@sheffield.ac.uk', 'wizapp4.0@gmail.com']
    # receivers = ['YOUR EMAIL HERE'] # for testing
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('wizapp4.0', "wizapp2023")

    # Send message with password to user
    # msg = EmailMessage()
    # msg.set_content(' Hi!\n\nThanks for wanting to use Wiz! \nPASSWORD: wiz2020.\n\nBest,\nChris Balzer')
    # msg['Subject'] = 'Password Request'
    # msg['From'] = 'Wiz <' + sender + '>'
    # msg['To'] = receivers

    # Send message to Peyman
    msg = EmailMessage()
    msg.set_content(' Hi Peyman,\n\nA user has requested access to Wiz.\n\nName: ' + first_name + ' ' +
        last_name + '\nEmail: ' + email + '\n\nBest,\nWiz Bot')
    msg['Subject'] = 'Wiz Password Request'
    msg['From'] = 'Wiz <wizapp4.0@gmail.com>'
    msg['To'] = receivers

    server.send_message(msg)
    server.quit()

    return '','','',1
