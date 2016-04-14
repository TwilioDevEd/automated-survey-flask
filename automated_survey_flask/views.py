from . import app
from . import question_view
from . import answer_view
from . import survey_view
from flask import render_template
from .models import Question


@app.route('/')
def root():
    questions = Question.query.all()
    return render_template('index.html', questions=questions)
