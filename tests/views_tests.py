from .base import BaseTest
from flask import url_for


class RootTest(BaseTest):

    def test_it_works(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)


class VoiceSurveysTest(BaseTest):

    def test_says_welcome_on_a_call(self):
        response = self.client.get('/voice')
        root = self.assertXmlDocument(response.data)

        welcome_text = 'Welcome to the %s survey' % self.survey.title
        self.assertEquals([welcome_text], root.xpath('./Say/text()'))

    def test_says_sorry_if_no_survey(self):
        self.delete_all_surveys()

        response = self.client.get('/voice')
        root = self.assertXmlDocument(response.data)

        sorry_text = 'Sorry, but there are no surveys to be answered.'
        self.assertEquals([sorry_text], root.xpath('./Say/text()'))

    def test_says_sorry_if_no_questions_for_this_survey(self):
        self.delete_all_questions()

        response = self.client.get('/voice')
        root = self.assertXmlDocument(response.data)

        sorry_text = 'Sorry, there are no questions for this survey.'
        self.assertEquals([sorry_text], root.xpath('./Say/text()'))

    def test_redirects_to_first_question(self):
        response = self.client.get('/voice')
        root = self.assertXmlDocument(response.data)

        first_question = self.questions[0]
        first_question_url = url_for('question', question_id=first_question.id)
        self.assertEquals([first_question_url],
                          root.xpath('./Redirect/text()'))


class QuestionTest(BaseTest):

    def test_first_question(self):
        first_question = self.questions[0]
        response = self.client.get(url_for('question',
                                   question_id=first_question.id))
        root = self.assertXmlDocument(response.data)

        self.assertXpathValues(root, '(./Say|./Message)/text()',
                               (first_question.content))
