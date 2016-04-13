from .base import BaseTest
from flask import url_for


class VoiceSurveysTest(BaseTest):

    def test_says_welcome_on_a_call(self):
        response = self.client.get('/voice')
        root = self.assertXmlDocument(response.data)

        welcome_text = 'Welcome to the %s survey' % self.survey.title
        self.assertEquals([welcome_text], root.xpath('./Say/text()'))

    def test_says_welcome_on_a_SMS_session(self):
        response = self.client.get('/message')
        root = self.assertXmlDocument(response.data)

        welcome_text = 'Welcome to the %s survey' % self.survey.title
        self.assertEquals([welcome_text], root.xpath('./Message/Body/text()'))

    def test_says_sorry_if_no_survey(self):
        self.delete_all_surveys()

        response = self.client.get('/voice')
        root = self.assertXmlDocument(response.data)

        sorry_text = 'Sorry, but there are no surveys to be answered.'
        self.assertEquals([sorry_text], root.xpath('./Say/text()'))

    def test_messages_sorry_if_no_survey_for_sms(self):
        self.delete_all_surveys()

        response = self.client.get('/message')
        root = self.assertXmlDocument(response.data)

        sorry_text = 'Sorry, but there are no surveys to be answered.'
        self.assertEquals([sorry_text], root.xpath('./Message/Body/text()'))

    def test_says_sorry_if_no_questions_for_this_survey(self):
        self.delete_all_questions()

        response = self.client.get('/voice')
        root = self.assertXmlDocument(response.data)

        sorry_text = 'Sorry, there are no questions for this survey.'
        self.assertEquals([sorry_text], root.xpath('./Say/text()'))

    def test_says_sorry_if_no_questions_for_this_survey_over_sms(self):
        self.delete_all_questions()

        response = self.client.get('/message')
        root = self.assertXmlDocument(response.data)

        sorry_text = 'Sorry, there are no questions for this survey.'
        self.assertEquals([sorry_text], root.xpath('./Message/Body/text()'))

    def test_redirects_to_first_question(self):
        response = self.client.get('/voice')
        root = self.assertXmlDocument(response.data)

        first_question = self.questions[0]
        first_question_url = url_for('question', question_id=first_question.id)
        self.assertEquals([first_question_url],
                          root.xpath('./Redirect/text()'))

    def test_redirects_to_first_question_over_sms(self):
        response = self.client.get('/message')
        root = self.assertXmlDocument(response.data)

        first_question = self.questions[0]
        first_question_url = url_for('question', question_id=first_question.id)
        self.assertEquals([first_question_url],
                          root.xpath('./Redirect/text()'))
