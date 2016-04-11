import unittest
from automated_survey_flask import parsers
from automated_survey_flask.models import Question


class ParserTests(unittest.TestCase):

    def setUp(self):
        self.survey_as_json = '{"title": "TDD Survey", "questions": [\
                {"body":"What is your name?", "type":"text"},\
                {"body":"What is your age?", "type":"numeric"},\
                {"body":"Do you know Python?", "type":"boolean"}]}'

    def test_parse_survey(self):
        survey = parsers.survey_from_json(self.survey_as_json)
        self.assertEquals("TDD Survey", survey.title)

    def test_survey_includes_questions(self):
        survey = parsers.survey_from_json(self.survey_as_json)
        self.assertEquals(3, survey.questions.count())

    def test_parse_question_title(self):
        questions = parsers.questions_from_json(self.survey_as_json)
        self.assertEquals("What is your name?", questions[0].content)

    def test_parse_text_question(self):
        questions = parsers.questions_from_json(self.survey_as_json)
        self.assertEquals(Question.TEXT, questions[0].kind)

    def test_parse_numeric_question(self):
        questions = parsers.questions_from_json(self.survey_as_json)
        self.assertEquals(Question.NUMERIC, questions[1].kind)

    def test_parse_boolean_questions(self):
        questions = parsers.questions_from_json(self.survey_as_json)
        self.assertEquals(Question.BOOLEAN, questions[2].kind)
