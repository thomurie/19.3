from flask import Flask, request, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey 

RESPONSES_1 = 'responses'

app = Flask(__name__)

app.config["SECRET_KEY"] = "oh-so-secret"

debug = DebugToolbarExtension(app)

@app.route('/')
def home():
    return render_template('index.html', title = satisfaction_survey.title, instructions= satisfaction_survey.instructions)

@app.route("/begin", methods=["POST"])
def begin():

    session[RESPONSES_1] = []

    return redirect("/questions/0")

@app.route(f"/questions/<int:num>")
def q(num):
    _responses = session.get(RESPONSES_1)

    if num != len(_responses):
        flash('Invalid HTML')
        return redirect(f"/questions/{len(_responses)}")

    if len(_responses) != len(satisfaction_survey.questions):
        return render_template('/question.html', question=satisfaction_survey.questions[len(_responses)], num=num)

    if len(_responses) == len(satisfaction_survey.questions):
        return redirect('/complete')
   
@app.route('/answer', methods=["POST"])
def a():
    user_input = request.form["select-choice"]
    _responses = session[RESPONSES_1]
    _responses.append(user_input)
    session[RESPONSES_1] = _responses

    if (len(_responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")
    
    else:
        return redirect(f"/questions/{len(_responses)}")

@app.route('/complete')
def c():

    return render_template('complete.html')