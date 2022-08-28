from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey
app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarenotcool"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
qnum = len(responses)
@app.route('/')
def home():
    return render_template('base.html')

@app.route('/questions/<int:qnum>')
def question(qnum):
    question = satisfaction_survey.questions[qnum-1].question
    choices = satisfaction_survey.questions[qnum-1].choices
    return render_template('questions.html', question = question, choices = choices)

@app.route('/answer', methods=["POST"])
def answer():
    choice = request.form['choice']
    if len(responses)<len(satisfaction_survey.questions)-1:
        responses.append(choice)
        return redirect (f'/questions/{len(responses)+1}')
    else:
        responses.append(choice)
        return render_template('thanks.html')

@app.route('/test')
def testing():
    return str(len(satisfaction_survey.questions))