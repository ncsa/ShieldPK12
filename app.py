import json

from flask import Flask, render_template, request, abort, redirect

from decisiontrees.module import Module

app = Flask(__name__)

# initialize the module
# TODO put the path in a config file
testing_decision = Module("decisiontrees/testing_decision.json")
with open("decisiontrees/testing_checklist.json", "r") as f:
    testing_checklist_ref = json.load(f)

distancing_decision = Module("decisiontrees/distancing_decision.json")
with open("decisiontrees/distancing_checklist.json", "r") as f:
    distancing_checklist_ref = json.load(f)

resource_foldername = "resources"


# reserve for landing page
@app.route('/', methods=['GET'])
def homepage():
    # TODO can have different landing page for different modules
    return render_template('landing.html')


@app.route('/<module>', methods=['GET'])
def module_homepage(module):
    # TODO can have different landing page for different modules
    return render_template('landing.html')


@app.route('/regress', methods=['GET'])
def regress():
    if request.args.get("module"):
        return redirect("/" + request.args.get("module") + "/questions")
    else:
        return redirect("/")


@app.route('/<module>/questions', methods=['GET'])
def questions(module):
    # TODO can have different template for different modules
    return render_template('questions.html')


@app.route('/<module>/questions', methods=['POST'])
def update_questions(module):
    if request.get_json() and request.get_json()['QID'] and 'qna' in request.get_json().keys():
        past_qna = request.get_json()['qna']
        question_id = request.get_json()['QID']

        if module == "testing-decision":
            decision = testing_decision
            checklist_ref = testing_checklist_ref
        elif module == "distancing-decision":
            decision = distancing_decision
            checklist_ref = distancing_checklist_ref
        elif module == "testing":
            decision = None
            checklist_ref = None
        elif module == "prevention":
            decision = None
            checklist_ref = None
        elif module == "cleaning":
            decision = None
            checklist_ref = None
        elif module == "data-infrastructure":
            decision = None
            checklist_ref = None
        else:
            decision = None
            checklist_ref = None
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

        if module == "testing-decision":
            decision = testing_decision
            checklist_ref = testing_checklist_ref
        elif module == "distancing-decision":
            decision = distancing_decision
            checklist_ref = distancing_checklist_ref
        elif module == "testing":
            decision = None
            checklist_ref = None
        elif module == "prevention":
            decision = None
            checklist_ref = None
        elif module == "cleaning":
            decision = None
            checklist_ref = None
        elif module == "data-infrastructure":
            decision = None
            checklist_ref = None
        else:
            decision = None
            checklist_ref = None
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
        page = None
        min_num_q = 999
        if module == "testing-decision":
            page = testing_decision.prev_page(prev_question_id)
            min_num_q = testing_decision.min_num_q
        elif module == "distancing-decision":
            page = distancing_decision.prev_page(prev_question_id)
            min_num_q = distancing_decision.min_num_q
        elif module == "testing":
            pass
        elif module == "prevention":
            pass
        elif module == "cleaning":
            pass
        elif module == "data-infrastructure":
            pass
        else:
            abort(404, "Module does not exist!")

        if page:
            return {"page": page, "minNumQ": min_num_q}
        else:
            abort(500, "Reach the beginning of the questions!")
    else:
        abort(403, 'need to provide the correct previous question id!')