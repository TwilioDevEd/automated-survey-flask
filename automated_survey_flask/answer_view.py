from . import app, db
from .models import Question, Answer
from flask import url_for, request
from twilio import twiml


@app.route('/answer/<question_id>', methods=['POST'])
def answer(question_id):
    question = Question.query.get(question_id)
    if question.kind == Question.TEXT:
        if 'TranscriptionText' in request.values:
            content_key = 'TranscriptionText'
        else:
            content_key = 'RecordingUrl'
    else:
        content_key = 'Digits'
    content = request.values[content_key]

    session_id = 42
    existing_answer = Answer.from_session_and_question(session_id, question)
    if existing_answer:
        existing_answer.content = content
        db.session.add(existing_answer)
    else:
        db.session.add(Answer(content=content,
                              question=question,
                              session_id=session_id))
    db.session.commit()

    response = twiml.Response()
    next_question = question.next()
    if next_question:
        response.redirect(url_for('question', question_id=next_question.id))
    else:
        response.say("Thank you for answering our survey. Good bye!")
    return str(response)
