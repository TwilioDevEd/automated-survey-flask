from .models import Survey, Question
import json


def survey_from_json(survey_json_string):
    survey_dict = json.loads(survey_json_string)
    survey = Survey(title=survey_dict['title'])
    survey.questions = questions_from_json(survey_json_string)
    return survey


def questions_from_json(survey_json_string):
    questions = []
    questions_dicts = json.loads(survey_json_string).get('questions')
    for question_dict in questions_dicts:
        body = question_dict['body']
        kind = question_dict['type']
        questions.append(Question(content=body, kind=kind))
    return questions
