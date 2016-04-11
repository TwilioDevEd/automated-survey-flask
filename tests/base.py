from xmlunittest import XmlTestCase
from automated_survey_flask.models import Survey, Question


class BaseTest(XmlTestCase):

    def setUp(self):
        from automated_survey_flask import app, db
        self.app = app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.db = db
        self.client = app.test_client()
        self.seed()

    def tearDown(self):
        self.delete_all_surveys()
        self.delete_all_questions()

    def delete_all_surveys(self):
        Survey.query.delete()

    def delete_all_questions(self):
        Question.query.delete()

    def seed(self):
        self.survey = Survey(title='Test')
        self.db.session.add(self.survey)

        all_kinds = [Question.TEXT, Question.BOOLEAN, Question.NUMERIC]
        for index, kind in enumerate(all_kinds):
            question = Question(content=('test %s' % str(index)), kind=kind)
            question.survey = self.survey
            self.db.session.add(question)

        self.db.session.commit()
        self.questions = self.survey.questions.order_by('id').all()
