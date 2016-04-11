from . import app
from twilio import twiml


@app.route('/')
def root():
    return ''
