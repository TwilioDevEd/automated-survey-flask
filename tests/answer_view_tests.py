from .base import BaseTest
from automated_survey_flask.models import Question, Answer
from flask import url_for


class AnswersTest(BaseTest):

    def test_answer_numeric_question(self):
        numeric_question = self.question_by_kind[Question.NUMERIC]
        data = {'Digits': '42'}
        self.client.post(url_for('answer',
                         question_id=numeric_question.id),
                         data=data)

        new_answer = Answer.query.first()
        self.assertTrue(new_answer, "No answer generated for numeric question")
        self.assertEquals(data['Digits'], new_answer.content)

    def test_answer_record_question(self):
        question = self.question_by_kind[Question.TEXT]
        data = {'RecordingUrl': 'http://example.com/recording.mp3'}
        self.client.post(url_for('answer',
                         question_id=question.id),
                         data=data)

        new_answer = Answer.query.first()
        self.assertTrue(new_answer, "No answer generated for numeric question")
        self.assertEquals(data['RecordingUrl'], new_answer.content)

    def test_answer_boolean_question(self):
        boolean_question = self.question_by_kind[Question.BOOLEAN]
        data = {'Digits': '1'}
        self.client.post(url_for('answer',
                         question_id=boolean_question.id),
                         data=data)

        new_answer = Answer.query.first()
        self.assertTrue(new_answer, "No answer generated for numeric question")
        self.assertEquals(data['Digits'], new_answer.content)

    def test_redirects_to_next_question_after_saving(self):
        first_question = self.questions[0]
        data = {'Digits': '42', 'RecordingUrl': 'notImportant'}
        response = self.client.post(url_for('answer',
                                            question_id=first_question.id),
                                    data=data)
        root = self.assertXmlDocument(response.data)

        next_question = self.questions[1]
        next_question_url = url_for('question', question_id=next_question.id)
        self.assertEquals([next_question_url],
                          root.xpath('./Redirect/text()'))
        self.assertEquals(['GET'],
                          root.xpath('./Redirect/@method'))

    def test_thanks_user_on_last_answer(self):
        last_question = self.questions[-1]
        data = {'Digits': '42', 'RecordingUrl': 'notImportant'}
        response = self.client.post(url_for('answer',
                                            question_id=last_question.id),
                                    data=data)
        root = self.assertXmlDocument(response.data)

        thank_you_text = 'Thank you for answering our survey. Good bye!'
        self.assertEquals([thank_you_text],
                          root.xpath('(./Say|./Message)/text()'))

    def test_transcription_callback_will_update(self):
        question = self.question_by_kind[Question.TEXT]
        data = {'RecordingUrl': 'http://example.com/itsok.mp3'}
        self.client.post(url_for('answer',
                         question_id=question.id),
                         data=data)
        data['TranscriptionText'] = 'I think it is ok.'
        self.client.post(url_for('answer',
                         question_id=question.id),
                         data=data)

        self.assertEquals(1, Answer.query.count(), "Answer duplicate on save!")
        new_answer = Answer.query.first()
        self.assertEquals(data['TranscriptionText'], new_answer.content)
