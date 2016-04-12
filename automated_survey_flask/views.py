from . import app
from . import question_view
from . import answer_view
from . import survey_view


@app.route('/')
def root():
    return ''
