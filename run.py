import urllib

import twilio.twiml
from twilio.rest import TwilioRestClient
from flask import Flask
from flask import request
from flask import redirect

import utils


app = Flask(__name__)
app.config.from_pyfile('config.py')
utils.init_db()
utils.make_recordings_directory()


@app.route('/', methods=['GET', 'POST'])
def index():
    resp = twilio.twiml.Response()
    resp.say('Welcome to the Labor Notifier.', voice='female')
    stamp = utils.get_timestamp()
    if stamp <= DEADLINE:
        resp.redirect(url='/api/register')
    else:
        resp.say('I\'m sorry, but the registration period has ended. Goodbye.', voice='female')
        resp.hangup()
    return str(resp)


@app.route('/api/register', methods=['GET', 'POST'])
def register():
    resp = twilio.twiml.Response()
    with resp.gather(numDigits=10, action='/api/save_number', method='POST') as g:
        g.say('To register to receive a phone call once the baby is born, please enter your '\
              'phone number. Enter the 3 digit area code, followed by the 7 digit number', voice='female')
    return str(resp)


@app.route('/api/save_number', methods=['GET', 'POST'])
def save_number():
    resp = twilio.twiml.Response()
    digits = request.values.get('Digits', None)
    digits_spaced = ' '.join(ch for ch in digits)
    digits = '+1' + digits
    resp.say('You entered the number ' + digits_spaced, voice='female')
    utils.insert_to_db(digits)
    resp.say('Thank you. You will receive a phone call at that number once labor begins.', voice='female')
    resp.say('Goodbye.', voice='female')
    resp.hangup()
    return str(resp)


@app.route('/notify', methods=['GET', 'POST'])
def notify():
    if request.form['Body'] == app.config['PHRASE']:
        client = TwilioRestClient(app.config['SID'], app.config['AUTH'])
        numbers = utils.get_all_numbers()
        for number in numbers:
            client.calls.create(to=number, from_=app.config['PHONE'],
                                url='http://'+app.config['IP']+':'+app.config['PORT']+'/api/notify')
        resp = twilio.twiml.Response()
        resp.message('Finished notifying all {} numbers'.format(len(numbers)))
        return str(resp)


@app.route('/api/notify', methods=['GET', 'POST'])
def notify_number():
    resp = twilio.twiml.Response()
    resp.say('This phone call is to notify you that Shalie Beck has finished labor.'\
             'Please don\'t bother calling as they most likely will not answer..', voice='female')
    with resp.gather(numDigits=1, action='/api/record_menu', method='POST') as g:
        g.say('If you would like to leave a message for the happy couple, please press 1. '\
              'If you do not wish to leave a message, press 2.', voice='female')
    return str(resp)


@app.route('/api/record_menu', methods=['GET', 'POST'])
def record_menu():
    digit = request.values.get('Digits', None)
    if digit == '1':
        return redirect('/api/record')
    else:
        resp = twilio.twiml.Response()
        resp.say('Thank you. Goodbye.', voice='female')
        resp.hangup()
        return str(resp)


@app.route('/api/record', methods=['GET', 'POST'])
def record():
    resp = twilio.twiml.Response()
    resp.say('Record your message after the tone. Make sure to state your name, and note '\
             'that the recording is only 30 seconds.', voice='female')
    resp.record(maxLength='30', action='/api/handle_recording')
    return str(resp)


@app.route('/api/handle_recording', methods=['GET', 'POST'])
def handle_recording():
    recording_url = request.values.get('RecordingUrl', None)
    resp = twilio.twiml.Response()
    resp.say('Thank you for leaving a message! Goodbye.', voice='female')
    resp.hangup()
    filename = 'recordings/'+request.values.get('To', None)+'.mp3'
    urllib.urlretrieve(recording_url+'.mp3', filename)
    return str(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['PORT'])

