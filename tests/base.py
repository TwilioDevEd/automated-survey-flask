from xmlunittest import XmlTestCase
from automated_survey_flask.models import Survey, Question, Answer


class BaseTest(XmlTestCase):

    def setUp(self):
        from automated_survey_flask import app, db
        self.app = app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.db = db
        self.client = self.app.test_client()
        self.seed()

    def tearDown(self):
        self.delete_all_surveys()
        self.delete_all_questions()
        self.delete_all_answers()

    def delete_all_surveys(self):
        Survey.query.delete()

    def delete_all_questions(self):
        Question.query.delete()

    def delete_all_answers(self):
        Answer.query.delete()

    def seed(self):
        self.survey = Survey(title='Test')
        self.db.save(self.survey)

        all_kinds = [Question.TEXT, Question.BOOLEAN, Question.NUMERIC]
        self.question_by_kind = {}
        for index, kind in enumerate(all_kinds):
            question = Question(content=('test %s' % str(index)), kind=kind)
            question.survey = self.survey
            self.db.save(question)
            self.question_by_kind[kind] = question

        self.questions = self.survey.questions.order_by('id').all()
