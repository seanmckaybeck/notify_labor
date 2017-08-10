import twilio.twiml
from twilio.rest import TwilioRestClient
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
import requests

import utils


app = Flask(__name__)
app.config.from_pyfile('config.py')
utils.init_db()
utils.make_recordings_directory()
MESSAGE = ''
voice = 'alice'


@app.route('/')
def index():
    return 'go away'


@app.route('/api/register', methods=['GET', 'POST'])
def register():
    resp = twilio.twiml.Response()
    resp.say('Welcome to the %s Notifier.' % app.config['BABY_NICKNAME'], voice=voice)
    with resp.gather(numDigits=10, action=url_for('confirm'), method='POST') as g:
        g.say('To register to receive a phone call once the baby is born, please enter your '\
              'phone number starting with the 3 digit area code, followed by the 7 digit number', voice=voice)
    return str(resp)


@app.route('/api/confirm', methods=['GET', 'POST'])
def confirm():
    resp = twilio.twiml.Response()
    digits = request.values.get('Digits', None)
    digits_spaced = ' '.join(ch for ch in digits)
    with resp.gather(numDigits=1, action=url_for('confirm_route', number=digits), method='GET') as g:
        g.say('You entered the number ' + digits_spaced + '. If this is correct, press 1. Otherwise, press 2.', voice=voice)
    return str(resp)


@app.route('/api/confirm_route')
def confirm_route():
    resp = twilio.twiml.Response()
    digit = request.args.get('Digits', None)
    if digit == '1':
        number = request.args.get('number', None)
        resp.redirect(url=url_for('text_or_call', number=number), method='GET')
        return str(resp)
    else:
        resp.redirect(url=url_for('register'))
        return str(resp)


@app.route('/api/text_or_call')
def text_or_call():
    resp = twilio.twiml.Response()
    number = request.args.get('number', None)
    with resp.gather(numDigits=1, action=url_for('save_number', number=number), method='GET') as g:
        g.say('If you would like to receive a text message, press 1. If you would like to receive a' \
              ' phone call, press 2.', voice=voice)
    return str(resp)


@app.route('/api/save_number')
def save_number():
    resp = twilio.twiml.Response()
    digit = request.args.get('Digits', None)
    number = request.args.get('number', None)
    text = None
    if digit == '1':
        text = True
    elif digit == '2':
        text = False
    else:
        resp.say(digit+' is not a valid choice.')
        resp.redirect(url_for('text_or_call', number=number), method='GET')
        return str(resp)
    number_spaced = ' '.join(ch for ch in number)
    number = '+1' + number
    utils.insert_to_db(number, text)
    resp.say('Thank you. You will receive a notification at that number once the baby is born.', voice=voice)
    resp.say('Goodbye.', voice=voice)
    resp.hangup()
    return str(resp)


@app.route('/notify', methods=['GET', 'POST'])
def notify():
    global MESSAGE
    sendmessage = False
    born = False
    client = TwilioRestClient(app.config['SID'], app.config['AUTHTOKEN'])

    if request.form['Body'].startswith(app.config['PHRASE']):
        MESSAGE = request.form['Body'].replace(app.config['PHRASE'], '', 1)
        sendmessage = True

    if request.form['Body'].startswith(app.config['PHRASE2']):
        MESSAGE = request.form['Body'].replace(app.config['PHRASE2'], '', 1)
        sendmessage = True
        born = True

    if sendmessage:
        numbers = utils.get_all_numbers()
        for number in numbers:
            if number[1] == 0:
                if born:
                    client.calls.create(to=number[0], from_=app.config['NUMBER'],
                                        url=app.config['URL']+'/api/notify')
            else:
                params = {'to': number[0], 'from_': app.config['NUMBER'], 'body': MESSAGE}
                if request.form['NumMedia'] == '1':
                    params['MediaUrl'] = request.form['MediaUrl0']
                client.messages.create(**params)
        resp = twilio.twiml.Response()
        resp.message('Finished notifying all {} numbers'.format(len(numbers)))
        return str(resp)

    if request.form['Body'].lower().startswith('join'):
        number = request.form['From']
        utils.insert_to_db(number, True)
        resp = twilio.twiml.Response()
        resp.message('You have been signed up for notifications!')
        return str(resp)

    resp = twilio.twiml.Response()
    resp.message('%s are busy right now.  Stay tuned for more updates :)' % app.config['PARENTS_NAME'])
    return str(resp)



@app.route('/api/notify', methods=['GET', 'POST'])
def notify_number():
    resp = twilio.twiml.Response()
    resp.pause(length=1)
    resp.say('Hello, this is your %s update. %s' % (app.config['BABY_NICKNAME'], MESSAGE), voice=voice)
    with resp.gather(numDigits=1, action=url_for('record_menu'), method='POST') as g:
        g.say('If you would like to leave a message for the happy family, please press 1. '\
              'If you do not wish to leave a message, you may hang up.', voice=voice)
    return str(resp)


@app.route('/api/record_menu', methods=['GET', 'POST'])
def record_menu():
    digit = request.values.get('Digits', None)
    if digit == '1':
        return redirect(url_for('record'))
    else:
        resp = twilio.twiml.Response()
        resp.say('Thank you. Goodbye.', voice=voice)
        resp.hangup()
        return str(resp)


@app.route('/api/record', methods=['GET', 'POST'])
def record():
    resp = twilio.twiml.Response()
    resp.say('Record your message after the tone. Make sure to state your name, and note '\
             'that the recording is only 30 seconds. When done, press the pound sign.', voice=voice)
    resp.record(maxLength='30', action=url_for('handle_recording'), finishOnKey='#')
    return str(resp)


@app.route('/api/handle_recording', methods=['GET', 'POST'])
def handle_recording():
    recording_url = request.values.get('RecordingUrl', None)
    resp = twilio.twiml.Response()
    resp.say('Thank you for leaving a message! Goodbye.', voice=voice)
    resp.hangup()
    filename = 'recordings/'+request.values.get('To', None)+'.mp3'
    r = requests.get(recording_url+'.mp3', stream=True)
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content():
            fd.write(chunk)
    return str(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['PORT'])

