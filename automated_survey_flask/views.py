from . import app
from .models import Survey
from twilio import twiml


@app.route('/')
def root():
    return ''


@app.route('/voice')
def voice_survey():
    response = twiml.Response()
    if not Survey.query.count():
        response.say('Sorry, but there are no surveys to be answered.')
        return str(response)
    welcome_text = 'Welcome to the %s survey' % Survey.query.first().title
    response.say(welcome_text)
    return str(response)
