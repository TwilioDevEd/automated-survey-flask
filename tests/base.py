import unittest


class BaseTest(unittest.TestCase):

    def setUp(self):
        from automated_survey_flask import app, db
        self.app = app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.db = db
        self.client = app.test_client()
