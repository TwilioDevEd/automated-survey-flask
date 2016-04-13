from .base import BaseTest
from automated_survey_flask.models import Question
from flask import url_for, session as flask_session


class QuestionsTest(BaseTest):

    def test_first_question_during_a_call(self):
        first_question = self.questions[0]
        response = self.client.get(url_for('question',
                                   question_id=first_question.id))
        root = self.assertXmlDocument(response.data)

        self.assertIn(first_question.content,
                      root.xpath('./Say/text()'))

    def test_first_question_over_sms(self):
        first_question = self.questions[0]
        response = self.client.get(url_for('question',
                                   question_id=first_question.id),
                                   data={'MessageSid': 'unique'})
        root = self.assertXmlDocument(response.data)

        self.assertIn(first_question.content,
                      root.xpath('./Message/Body/text()'))

    def test_current_question_being_answered_goes_to_session(self):
        first_question = self.questions[0]
        with self.app.test_client() as client:
            client.get(url_for('question',
                               question_id=first_question.id),
                       data={'MessageSid': 'unique'})
            session = flask_session
            self.assertEquals(first_question.id, session['question_id'])

    def test_gather_keys_on_numeric_question_during_a_call(self):
        numeric_question = self.question_by_kind[Question.NUMERIC]
        response = self.client.get(url_for('question',
                                   question_id=numeric_question.id))
        root = self.assertXmlDocument(response.data)

        answer_url = url_for('answer', question_id=numeric_question.id)
        self.assertEquals([answer_url], root.xpath('./Gather/@action'))

    def test_record_on_text_questions_during_a_call(self):
        text_question = self.question_by_kind[Question.TEXT]
        response = self.client.get(url_for('question',
                                   question_id=text_question.id))
        root = self.assertXmlDocument(response.data)

        answer_url = url_for('answer', question_id=text_question.id)
        self.assertEquals([answer_url], root.xpath('./Record/@action'))

    def test_transcription_is_enabled_for_text_questions_during_a_call(self):
        text_question = self.question_by_kind[Question.TEXT]
        response = self.client.get(url_for('question',
                                   question_id=text_question.id))
        root = self.assertXmlDocument(response.data)

        answer_transcription_url = url_for('answer_transcription',
                                           question_id=text_question.id)
        self.assertEquals([answer_transcription_url],
                          root.xpath('./Record/@transcribeCallback'))

    def test_gather_keys_on_boolean_question_during_a_call(self):
        boolean_question = self.question_by_kind[Question.BOOLEAN]
        response = self.client.get(url_for('question',
                                   question_id=boolean_question.id))
        root = self.assertXmlDocument(response.data)

        answer_url = url_for('answer', question_id=boolean_question.id)
        self.assertEquals([answer_url], root.xpath('./Gather/@action'))
