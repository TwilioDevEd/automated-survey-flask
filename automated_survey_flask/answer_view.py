from . import app, db
from .models import Question, Answer
from flask import url_for, request, session
from twilio import twiml


@app.route('/answer/<question_id>', methods=['POST'])
def answer(question_id):
    question = Question.query.get(question_id)

    db.save(Answer(content=extract_content(question),
                   question=question,
                   session_id=session_id()))

    next_question = question.next()
    if next_question:
        return redirect_twiml(next_question)
    else:
        return goodbye_twiml()


def extract_content(question):
    if is_sms_request():
        return request.values['Body']
    elif question.kind == Question.TEXT:
        return 'Transcription in progress.'
    else:
        return request.values['Digits']


def redirect_twiml(question):
    response = twiml.Response()
    response.redirect(url_for('question', question_id=question.id),
                      method='GET')
    return str(response)


def goodbye_twiml():
    response = twiml.Response()
    if is_sms_request():
        response.message("Thank you for answering our survey. Good bye!")
    else:
        response.say("Thank you for answering our survey. Good bye!")
        response.hangup()
    if 'question_id' in session:
        del session['question_id']
    return str(response)


def is_sms_request():
    return 'MessageSid' in request.values.keys()


@app.route('/answer/transcription/<question_id>', methods=['POST'])
def answer_transcription(question_id):
    session_id = request.values['CallSid']
    content = request.values['TranscriptionText']
    Answer.update_content(session_id, question_id, content)
    return ''


def session_id():
    return request.values.get('CallSid') or request.values['MessageSid']
