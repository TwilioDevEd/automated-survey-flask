from . import app
from . import question_view  # noqa F401
from . import answer_view   # noqa F401
from . import survey_view   # noqa F401
from flask import render_template
from .models import Question


@app.route('/')
def root():
    questions = Question.query.all()
    return render_template('index.html', questions=questions)
