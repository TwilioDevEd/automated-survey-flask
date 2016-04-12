from .base import BaseTest
from automated_survey_flask.models import Question
from flask import url_for


class QuestionsTest(BaseTest):

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

    def test_transcription_is_enabled_for_text_questions(self):
        text_question = self.question_by_kind[Question.TEXT]
        response = self.client.get(url_for('question',
                                   question_id=text_question.id))
        root = self.assertXmlDocument(response.data)

        answer_url = url_for('answer', question_id=text_question.id)
        self.assertEquals([answer_url],
                          root.xpath('./Record/@transcribeCallback'))

    def test_gather_keys_on_boolean_question(self):
        boolean_question = self.question_by_kind[Question.BOOLEAN]
        response = self.client.get(url_for('question',
                                   question_id=boolean_question.id))
        root = self.assertXmlDocument(response.data)

        answer_url = url_for('answer', question_id=boolean_question.id)
        self.assertEquals([answer_url], root.xpath('./Gather/@action'))
