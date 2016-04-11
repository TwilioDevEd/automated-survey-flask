from . import app, db
from .models import Survey, Question, Answer
from flask import url_for, request
from twilio import twiml


@app.route('/')
def root():
    return ''


@app.route('/voice')
def voice_survey():
    response = twiml.Response()
    survey = Survey.query.first()
    if not survey:
        response.say('Sorry, but there are no surveys to be answered.')
        return str(response)

    if not survey.questions.count():
        response.say('Sorry, there are no questions for this survey.')
        return str(response)

    welcome_text = 'Welcome to the %s survey' % survey.title
    response.say(welcome_text)

    first_question = survey.questions.order_by('id').first()
    response.redirect(url_for('question', question_id=first_question.id))

    return str(response)


@app.route('/question/<question_id>')
def question(question_id):
    question = Question.query.get(question_id)
    response = twiml.Response()
    response.say(question.content)

    action_url = url_for('answer', question_id=question_id)
    if question.kind == Question.TEXT:
        response.record(action=action_url)
    else:
        response.gather(action=action_url)
    return str(response)


@app.route('/answer/<question_id>', methods=['POST'])
def answer(question_id):
    question = Question.query.get(question_id)
    if question.kind == Question.TEXT:
        content_key = 'RecordingUrl'
    else:
        content_key = 'Digits'
    content = request.form[content_key]
    db.session.add(Answer(content=content,
                          question=question))
    db.session.commit()
    response = twiml.Response()
    return str(response)
