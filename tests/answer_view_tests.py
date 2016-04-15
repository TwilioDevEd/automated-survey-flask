from .base import BaseTest
from automated_survey_flask.models import Question, Answer
from flask import url_for


class AnswersTest(BaseTest):

    def post_answer_for_question_kind(self, kind, is_sms=False):
        self.data = {('MessageSid' if is_sms else 'CallSid'): 'unique'}
        if is_sms:
            self.data['Body'] = '42'
        if kind == Question.NUMERIC:
            self.data['Digits'] = '42'
        elif kind == Question.BOOLEAN:
            self.data['Digits'] = '1'
        elif kind == Question.TEXT:
            self.data['RecordingUrl'] = 'example.com/yours.mp3'
        question_id = self.question_by_kind[kind].id
        response = self.client.post(url_for('answer',
                                            question_id=question_id),
                                    data=self.data)
        return self.assertXmlDocument(response.data)

    def test_answer_numeric_question_during_a_call(self):
        self.post_answer_for_question_kind(Question.NUMERIC)

        new_answer = Answer.query.first()
        self.assertTrue(new_answer, "No answer generated for numeric question")
        self.assertEquals(self.data['Digits'], new_answer.content)

    def test_answer_numeric_question_over_sms(self):
        self.post_answer_for_question_kind(Question.NUMERIC, is_sms=True)

        new_answer = Answer.query.first()
        self.assertTrue(new_answer, "No answer generated for numeric question")
        self.assertEquals(self.data['Body'], new_answer.content)

    def test_answer_record_question_stores_transcription_in_progress(self):
        self.post_answer_for_question_kind(Question.TEXT)

        new_answer = Answer.query.first()
        self.assertTrue(new_answer, "No answer generated for numeric question")
        self.assertEquals('Transcription in progress.', new_answer.content)

    def test_answer_boolean_question_during_a_call(self):
        self.post_answer_for_question_kind(Question.BOOLEAN)

        new_answer = Answer.query.first()
        self.assertTrue(new_answer, "No answer generated for numeric question")
        self.assertEquals(self.data['Digits'], new_answer.content)

    def test_answer_boolean_question_over_sms(self):
        self.post_answer_for_question_kind(Question.BOOLEAN, is_sms=True)

        new_answer = Answer.query.first()
        self.assertTrue(new_answer, "No answer generated for boolean question")
        self.assertEquals(self.data['Body'], new_answer.content)

    def test_redirects_to_next_question_after_saving(self):
        first_question = self.questions[0]
        root = self.post_answer_for_question_kind(first_question.kind)

        next_question = self.questions[1]
        next_question_url = url_for('question', question_id=next_question.id)
        self.assertEquals([next_question_url],
                          root.xpath('./Redirect/text()'))
        self.assertEquals(['GET'],
                          root.xpath('./Redirect/@method'))

    def test_thanks_user_on_last_answer(self):
        last_question = self.questions[-1]
        root = self.post_answer_for_question_kind(last_question.kind)

        thank_you_text = 'Thank you for answering our survey. Good bye!'
        self.assertEquals([thank_you_text],
                          root.xpath('(./Say|./Message)/text()'))

    def test_hangup_on_last_answer_during_a_call(self):
        last_question = self.questions[-1]
        root = self.post_answer_for_question_kind(last_question.kind)

        self.assertEquals(1, len(root.xpath('./Hangup')))

    def test_transcription_callback_will_update(self):
        question = self.question_by_kind[Question.TEXT]
        self.post_answer_for_question_kind(question.kind)
        self.data['TranscriptionText'] = 'I think it is ok.'
        self.client.post(url_for('answer_transcription',
                         question_id=question.id),
                         data=self.data)

        self.assertEquals(1, Answer.query.count())
        new_answer = Answer.query.first()
        self.assertEquals(self.data['TranscriptionText'], new_answer.content)
