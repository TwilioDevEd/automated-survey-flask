from . import app
from twilio import twiml
from .models import Question
from flask import url_for


@app.route('/question/<question_id>')
def question(question_id):
    question = Question.query.get(question_id)
    response = twiml.Response()
    response.say(question.content)
    response.say(VOICE_INSTRUCTIONS[question.kind])

    action_url = url_for('answer', question_id=question_id)
    if question.kind == Question.TEXT:
        response.record(action=action_url,
                        transcribeCallback=action_url)
    else:
        response.gather(action=action_url)
    return str(response)

VOICE_INSTRUCTIONS = {
        Question.TEXT: 'Please record your answer after the beep and then hit the pound sign',
        Question.BOOLEAN: 'Please press the one key for yes and the zero key for no and then hit the pound sign',
        Question.NUMERIC: 'Please press a number between 1 and 10 and then hit the pound sign'
}
