import unittest
from automated_survey_flask.models import Survey


class BaseTest(unittest.TestCase):

    def setUp(self):
        from automated_survey_flask import app, db
        self.app = app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.db = db
        self.client = app.test_client()
        self.seed()

    def tearDown(self):
        Survey.query.delete()

    def seed(self):
        self.survey = Survey(title='Test')
        self.db.session.add(self.survey)
