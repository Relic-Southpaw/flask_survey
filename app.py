# this calls all the tools needed
# also ties in the surveys.py to this code.
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey
app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarenotcool"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# this is where we store the responses
# a variable to help with functions
# route to home page, has survey start button.
@app.route('/')
def home():
    return render_template('base.html')
# pulls questions and answers from surveys.py and generates them
@app.route(f'/questions/<int:qnum>')
def question(qnum):
# the if else is there to assure they answer the questions in order.  
# Prevents skipping around.
    # this first will check if they answered all the questions already.
    print(f"{qnum} is qnum")
    #the session way to make the cookie session usable
    responses = session['response']
    session['response'] = responses
    if qnum <= len(satisfaction_survey.questions):
        if qnum == len(responses)+1:
            question = satisfaction_survey.questions[qnum-1].question
            choices = satisfaction_survey.questions[qnum-1].choices
            return render_template('questions.html', question = question, choices = choices)
        else:
            # this if/else responds if the URL is messed with.
            if qnum != 0:
                return redirect(f'/questions/{len(responses)+1}')
            else:
            # flashes a message if they try to jump questions.
                flash("Don't mess with the URL. . . ")
                return redirect(f'/questions/{len(responses)+1}')

    # this else will thank them if they already answered all the questions and try to start again.
    else:
        return render_template('thanks.html')


# this route processes the answers and adds them to the responses list.
@app.route('/answer', methods=["POST"])
def answer():
    choice = request.form['choice']
    #the session way to make the cookie session usable
    responses = session['response']
    responses.append(choice)
    session['response'] = responses
    print (f'{len(responses)} is len')
# if else checks the length of survey and when they complete all questions
    if (len(responses)<len(satisfaction_survey.questions)):
        return redirect (f'/questions/{len(responses)+1}')
    else:
        # responses.append(choice)
# it returns a thanks page to thank them for taking the survey
        return render_template('thanks.html')


@app.route('/sessions-setup', methods=["POST"])
def session_starting():
    responses = session['response']
    responses = []
    session['response'] = responses
    return redirect('/questions/1')


# I was using this route to test things in the browser to set variables.
@app.route('/test')
def testing():
    eggs = session.get('response')
    # return str(len(satisfaction_survey.questions))
    return render_template('thanks.html', eggs = eggs)

