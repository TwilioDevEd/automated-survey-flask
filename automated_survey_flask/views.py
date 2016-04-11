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
    response.redirect(url_for('question', question_id=first_question.id),
                      method='GET')

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
    existing_answer = Answer.query.filter(Answer.question == question).first()
    if existing_answer:
        existing_answer.content = content
        db.session.add(existing_answer)
    else:
        db.session.add(Answer(content=content,
                              question=question))
    db.session.commit()
    response = twiml.Response()
    next_question = question.next()
    if next_question:
        response.redirect(url_for('question', question_id=next_question.id))
    else:
        response.say("Thank you for answering our survey. Good bye!")
    return str(response)
