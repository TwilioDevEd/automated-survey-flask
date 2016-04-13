from . import app, db
from .models import Question, Answer
from flask import url_for, request
from twilio import twiml


@app.route('/answer/<question_id>', methods=['POST'])
def answer(question_id):
    question = Question.query.get(question_id)
    if question.kind == Question.TEXT:
        content = 'Transcription in progress.'
    else:
        content = request.values['Digits']

    session_id = request.values['CallSid']
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
        response.say("Thank you for answering our survey. Good bye!")
        response.hangup()
    return str(response)


@app.route('/answer/transcription/<question_id>', methods=['POST'])
def answer_transcription(question_id):
    session_id = request.values['CallSid']
    existing_answer = Answer.from_session_and_question(session_id, question_id)
    existing_answer.content = request.values['TranscriptionText']
    db.session.add(existing_answer)
    db.session.commit()
    return ''
