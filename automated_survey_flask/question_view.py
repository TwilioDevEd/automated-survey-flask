from . import app
from twilio import twiml
from .models import Question
from flask import url_for, request, session


@app.route('/question/<question_id>')
def question(question_id):
    question = Question.query.get(question_id)
    session['question_id'] = question.id
    if not is_sms_request():
        return voice_twiml(question)
    else:
        return sms_twiml(question)


def is_sms_request():
    return 'MessageSid' in request.values.keys()


def voice_twiml(question):
    response = twiml.Response()
    response.say(question.content)
    response.say(VOICE_INSTRUCTIONS[question.kind])

    action_url = url_for('answer', question_id=question.id)
    transcription_url = url_for('answer_transcription',
                                question_id=question.id)
    if question.kind == Question.TEXT:
        response.record(action=action_url,
                        transcribeCallback=transcription_url)
    else:
        response.gather(action=action_url)
    return str(response)

VOICE_INSTRUCTIONS = {
        Question.TEXT: 'Please record your answer after the beep and then hit the pound sign',
        Question.BOOLEAN: 'Please press the one key for yes and the zero key for no and then hit the pound sign',
        Question.NUMERIC: 'Please press a number between 1 and 10 and then hit the pound sign'
}


def sms_twiml(question):
    response = twiml.Response()
    response.message(question.content)
    response.message(SMS_INSTRUCTIONS[question.kind])
    return str(response)

SMS_INSTRUCTIONS = {
        Question.TEXT: 'Please type your answer',
        Question.BOOLEAN: 'Please type 1 for yes and 0 for no',
        Question.NUMERIC: 'Please type a number between 1 and 10'
}
