from .base import BaseTest
from automated_survey_flask.models import Question, Answer
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
