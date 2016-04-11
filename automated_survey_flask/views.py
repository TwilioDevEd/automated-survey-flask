from . import app
from twilio import twiml


@app.route('/')
def root():
    return ''


@app.route('/voice')
def voice_survey():
    response = twiml.Response()
    response.say("Welcome!")
    return str(response)
