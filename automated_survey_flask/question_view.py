from . import app
from twilio import twiml
from .models import Question
from flask import url_for


@app.route('/question/<question_id>')
def question(question_id):
    question = Question.query.get(question_id)
    response = twiml.Response()
    response.say(question.content)

    action_url = url_for('answer', question_id=question_id)
    if question.kind == Question.TEXT:
        response.record(action=action_url,
                        transcribeCallback=action_url)
    else:
        response.gather(action=action_url)
    return str(response)
