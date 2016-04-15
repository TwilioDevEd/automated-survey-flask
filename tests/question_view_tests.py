from .base import BaseTest
from automated_survey_flask.models import Question
from flask import url_for, session as flask_session


class QuestionsTest(BaseTest):

    def get_question_as_xml(self, question, client=None, data=None):
        client = client or self.client
        response = client.get(url_for('question',
                                      question_id=question.id),
                              data=data)
        return self.assertXmlDocument(response.data)

    def test_first_question_during_a_call(self):
        first_question = self.questions[0]
        root = self.get_question_as_xml(first_question)

        self.assertIn(first_question.content,
                      root.xpath('./Say/text()'))

    def test_first_question_over_sms(self):
        first_question = self.questions[0]
        data = {'MessageSid': 'unique'}
        root = self.get_question_as_xml(first_question, data=data)

        self.assertIn(first_question.content,
                      root.xpath('./Message/Body/text()'))

    def test_current_question_being_answered_goes_to_session(self):
        first_question = self.questions[0]
        with self.app.test_client() as client:
            self.get_question_as_xml(first_question, client=client)
            self.assertEquals(first_question.id, flask_session['question_id'])

    def test_gather_keys_on_numeric_question_during_a_call(self):
        numeric_question = self.question_by_kind[Question.NUMERIC]
        root = self.get_question_as_xml(numeric_question)

        answer_url = url_for('answer', question_id=numeric_question.id)
        self.assertEquals([answer_url], root.xpath('./Gather/@action'))

    def test_record_on_text_questions_during_a_call(self):
        text_question = self.question_by_kind[Question.TEXT]
        root = self.get_question_as_xml(text_question)

        answer_url = url_for('answer', question_id=text_question.id)
        self.assertEquals([answer_url], root.xpath('./Record/@action'))

    def test_transcription_is_enabled_for_text_questions_during_a_call(self):
        text_question = self.question_by_kind[Question.TEXT]
        root = self.get_question_as_xml(text_question)

        answer_transcription_url = url_for('answer_transcription',
                                           question_id=text_question.id)
        self.assertEquals([answer_transcription_url],
                          root.xpath('./Record/@transcribeCallback'))

    def test_gather_keys_on_boolean_question_during_a_call(self):
        boolean_question = self.question_by_kind[Question.BOOLEAN]
        root = self.get_question_as_xml(boolean_question)

        answer_url = url_for('answer', question_id=boolean_question.id)
        self.assertEquals([answer_url], root.xpath('./Gather/@action'))
