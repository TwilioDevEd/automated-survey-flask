from . import app
from .models import Survey
from flask import url_for
from twilio import twiml


@app.route('/voice')
def voice_survey():
    response = twiml.Response()

    survey = Survey.query.first()
    if not survey:
        response.say('Sorry, but there are no surveys to be answered.')
        return str(response)
    elif not survey.has_questions:
        response.say('Sorry, there are no questions for this survey.')
        return str(response)

    welcome_text = 'Welcome to the %s survey' % survey.title
    response.say(welcome_text)

    first_question = survey.questions.order_by('id').first()
    first_question_url = url_for('question', question_id=first_question.id)
    response.redirect(first_question_url, method='GET')
    return str(response)
