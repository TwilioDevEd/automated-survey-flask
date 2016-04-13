from . import app, db
from .models import Question, Answer
from flask import url_for, request, session
from twilio import twiml


@app.route('/answer/<question_id>', methods=['POST'])
def answer(question_id):
    question = Question.query.get(question_id)
    if is_sms():
        content = request.values['Body']
    elif question.kind == Question.TEXT:
        content = 'Transcription in progress.'
    else:
        content = request.values['Digits']

    session_id = request.values.get('CallSid') or request.values['MessageSid']
    db.session.add(Answer(content=content,
                   question=question,
                   session_id=session_id))
    db.session.commit()

    response = twiml.Response()
    next_question = question.next()
    if next_question:
        response.redirect(url_for('question', question_id=next_question.id),
                          method='GET')
    else:
        if is_sms():
            response.message("Thank you for answering our survey. Good bye!")
        else:
            response.say("Thank you for answering our survey. Good bye!")
            response.hangup()
        if 'question_id' in session:
            del session['question_id']
    return str(response)


def is_sms():
    return 'MessageSid' in request.values.keys()


@app.route('/answer/transcription/<question_id>', methods=['POST'])
def answer_transcription(question_id):
    session_id = request.values['CallSid']
    content = request.values['TranscriptionText']
    Answer.update_content(session_id, question_id, content)
    return ''
