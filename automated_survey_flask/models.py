from automated_survey_flask import db


class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    questions = db.relationship('Question', backref='survey', lazy='dynamic')

    def __init__(self, title):
        self.title = title


class Question(db.Model):
    __tablename__ = 'questions'

    TEXT = 'text'
    NUMERIC = 'numeric'
    BOOLEAN = 'boolean'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    kind = db.Column(db.Enum(TEXT, NUMERIC, BOOLEAN,
                             name='question_kind'))
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __init__(self, content, kind=TEXT):
        self.content = content
        self.kind = kind


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __init__(self, content):
        self.content = content
