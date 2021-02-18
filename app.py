import json

from flask import Flask, render_template, request, abort, redirect

from decisiontrees.module import Module

app = Flask(__name__)
app.add_url_rule('/static/css/', endpoint='css', view_func=app.send_static_file)
app.add_url_rule('/static/js/', endpoint='js', view_func=app.send_static_file)
app.add_url_rule('/static/img/', endpoint='img', view_func=app.send_static_file)

# initialize the module
# TODO put the path in a config file
testing_decision = Module("decisiontrees/testing_decision.json")
with open("decisiontrees/testing_checklist.json", "r") as f:
    testing_checklist_ref = json.load(f)

distancing_decision = Module("decisiontrees/distancing_decision.json")
with open("decisiontrees/distancing_checklist.json", "r") as f:
    distancing_checklist_ref = json.load(f)

ventilation_decision = Module("decisiontrees/ventilation_decision.json")
with open("decisiontrees/ventilation_checklist.json", "r") as f:
    ventilation_checklist_ref = json.load(f)

mask_decision = Module("decisiontrees/mask_decision.json")
with open("decisiontrees/mask_checklist.json", "r") as f:
    mask_checklist_ref = json.load(f)

cleaning_decision = Module("decisiontrees/cleaning_decision.json")
with open("decisiontrees/cleaning_checklist.json", "r") as f:
    cleaning_checklist_ref = json.load(f)

IT_decision = Module("decisiontrees/IT_decision.json")
with open("decisiontrees/IT_checklist.json", "r") as f:
    IT_checklist_ref = json.load(f)

resource_foldername = "resources"


# reserve for landing page
@app.route('/', methods=['GET'])
def homepage():
    return render_template("landing.html")


@app.route('/error', methods=['GET'])
def error():
    return render_template("error.html")

# @app.route('/<module>', methods=['GET'])
# def module_homepage(module):
#     # TODO can have different landing page for different modules
#     return render_template('landing.html')


@app.route('/<module>/questions', methods=['GET'])
def questions(module):
    # TODO can have different template for different modules
    return render_template('questions.html')


@app.route('/<module>/questions', methods=['POST'])
def update_questions(module):
    if request.get_json() and request.get_json()['QID'] and 'qna' in request.get_json().keys():
        past_qna = request.get_json()['qna']
        question_id = request.get_json()['QID']

        decision, checklist_ref = _populate(module)
        if decision is None or checklist_ref is None:
            abort(404, "Module does not exist!")

        if question_id != "null":
            page = decision.get_current_page(question_id)
            min_num_q = testing_decision.min_num_q
            if page:
                return {"page": page, "minNumQ": min_num_q}
            else:
                abort(500, "Page does not exist!")
        else:
            # reaching to the end
            report = decision.generate_qna_report(past_qna)
            checklist = decision.compile_checklist(past_qna, checklist_ref)
            return {
                "report": report,
                "checklist": checklist
            }

    else:
        abort(403, 'Incomplete question id!')


@app.route('/<module>/next', methods=['POST'])
def next_question(module):
    if request.get_json() and request.get_json()['QID'] and request.get_json()['AID'] \
            and 'qna' in request.get_json().keys():
        past_qna = request.get_json()['qna']
        question_id = request.get_json()['QID']
        answer_id_list = request.get_json()['AID']

        # add current question and answer to the past qna list for further critera
        if {"QID": question_id, "AID": answer_id_list} not in past_qna:
            past_qna.insert(0, {"QID": question_id, "AID": answer_id_list})

        decision, checklist_ref = _populate(module)
        if decision is None or checklist_ref is None:
            abort(404, "Module does not exist!")

        page = decision.next_page(question_id, answer_id_list, past_qna)
        min_num_q = decision.min_num_q
        if page:
            # rendering next page
            return {"page": page, "minNumQ": min_num_q}
        else:
            # reaching to the end
            report = decision.generate_qna_report(past_qna)
            checklist = decision.compile_checklist(past_qna, checklist_ref)
            return {
                "report": report,
                "checklist":checklist
            }
    else:
        abort(403, 'Incomplete question id and answer id!')


@app.route('/<module>/prev', methods=['POST'])
def prev_question(module):
    if request.get_json() and request.get_json()['prevQID']:
        prev_question_id = request.get_json()['prevQID']
        decision, checklist_ref = _populate(module)
        if decision is None or checklist_ref is None:
            abort(404, "Module does not exist!")

        page = decision.prev_page(prev_question_id)
        min_num_q = decision.min_num_q
        if page:
            return {"page": page, "minNumQ": min_num_q}
        else:
            abort(500, "Reach the beginning of the questions!")
    else:
        abort(403, 'need to provide the correct previous question id!')


def _populate(module):
    if module == "testing":
        decision = testing_decision
        checklist_ref = testing_checklist_ref
    elif module == "distancing":
        decision = distancing_decision
        checklist_ref = distancing_checklist_ref
    elif module == "ventilation":
        decision = ventilation_decision
        checklist_ref = ventilation_checklist_ref
    elif module == "mask":
        decision = mask_decision
        checklist_ref = mask_checklist_ref
    elif module == "cleaning":
        decision = cleaning_decision
        checklist_ref = cleaning_checklist_ref
    elif module == "IT":
        decision = IT_decision
        checklist_ref = IT_checklist_ref
    else:
        decision = None
        checklist_ref = None

    return decision, checklist_ref