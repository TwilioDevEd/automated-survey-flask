from .base import BaseTest
from automated_survey_flask.models import Question
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

        self.assertEquals([first_question.content],
                          root.xpath('(./Say|./Message)/text()'))

    def test_gather_keys_on_numeric_question(self):
        numeric_question = self.question_by_kind[Question.NUMERIC]
        response = self.client.get(url_for('question',
                                   question_id=numeric_question.id))
        root = self.assertXmlDocument(response.data)

        answer_url = url_for('answer', question_id=numeric_question.id)
        self.assertEquals([answer_url], root.xpath('./Gather/@action'))

    def test_record_on_text_questions(self):
        text_question = self.question_by_kind[Question.TEXT]
        response = self.client.get(url_for('question',
                                   question_id=text_question.id))
        root = self.assertXmlDocument(response.data)

        answer_url = url_for('answer', question_id=text_question.id)
        self.assertEquals([answer_url], root.xpath('./Record/@action'))

    def test_gather_keys_on_boolean_question(self):
        boolean_question = self.question_by_kind[Question.BOOLEAN]
        response = self.client.get(url_for('question',
                                   question_id=boolean_question.id))
        root = self.assertXmlDocument(response.data)

        answer_url = url_for('answer', question_id=boolean_question.id)
        self.assertEquals([answer_url], root.xpath('./Gather/@action'))
