from flask import Flask, request, render_template, flash, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey 

app = Flask(__name__)

app.config["SECRET_KEY"] = "oh-so-secret"

debug = DebugToolbarExtension(app)

RESPONSES = []

@app.route('/')
def home():
    RESPONSES.clear()
    return render_template('index.html', title = satisfaction_survey.title, instructions= satisfaction_survey.instructions)

@app.route('/begin')
def begin():
    return redirect(f"/questions/{len(RESPONSES)}")

@app.route(f"/questions/<int:num>")
def q(num):
    if num != len(RESPONSES):
        flash('Invalid HTML')
        return redirect(f"/questions/{len(RESPONSES)}")
    if len(RESPONSES) != len(satisfaction_survey.questions):
        return render_template('/question.html', question=satisfaction_survey.questions[len(RESPONSES)], num=num)
    if len(RESPONSES) == len(satisfaction_survey.questions):
        return redirect('/complete')
   
@app.route('/answer')
def a():
    RESPONSES.append(request.args["select-choice"])
    print(RESPONSES)

    return redirect(f"/questions/{len(RESPONSES)}")

@app.route('/complete')
def c():
    return render_template('complete.html')