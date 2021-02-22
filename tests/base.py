from xmlunittest import XmlTestCase
from automated_survey_flask.models import Survey, Question, Answer

from automated_survey_flask import app, db


class BaseTest(XmlTestCase):
    def setUp(self):
        self.client = app.test_client()
        db.create_all()
        self.seed()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @staticmethod
    def delete_all_surveys():
        Survey.query.delete()

    @staticmethod
    def delete_all_questions():
        Question.query.delete()

    @staticmethod
    def delete_all_answers():
        Answer.query.delete()

    def seed(self):
        self.survey = Survey(title='Test')
        db.session.add(self.survey)

        all_kinds = [Question.TEXT, Question.BOOLEAN, Question.NUMERIC]
        self.question_by_kind = {}
        for index, kind in enumerate(all_kinds):
            question = Question(content=('test %s' % str(index)), kind=kind)
            question.survey = self.survey
            db.session.add(question)
            self.question_by_kind[kind] = question

        db.session.commit()

        self.questions = self.survey.questions.order_by('id').all()
