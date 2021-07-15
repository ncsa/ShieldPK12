import json
import os
from flask import Flask, render_template, request, abort, redirect

from decisiontrees.module import Module

app = Flask(__name__)
app.add_url_rule('/static/css/', endpoint='css', view_func=app.send_static_file)
app.add_url_rule('/static/js/', endpoint='js', view_func=app.send_static_file)
app.add_url_rule('/static/img/', endpoint='img', view_func=app.send_static_file)

# initialize the module once
modules = {}
module_descriptions = []
module_config_home = "decisiontrees"
for module_config_file in os.listdir(module_config_home):
    module_config_file_full_path = os.path.join(module_config_home, module_config_file)
    if os.path.isfile(module_config_file_full_path) and module_config_file_full_path.endswith(".json"):
        with open(module_config_file_full_path, "r") as f:
            config = json.load(f)
            if "moduleName" in config:
                module_name = config["moduleName"]
                module_descriptions.append({"moduleName": module_name,
                                            "moduleDescription": config.get("moduleDescription", "")})
                modules[module_name] = {}
                modules[module_name]["decision"] = Module(config.get("moduleContent", {}))
                modules[module_name]["checklist"] = config.get("checklist", {})
            else:
                print(module_config_file_full_path, "is missing required field module name. Skip...")


def _populate(module_name):
    decision = modules.get(module_name, {}).get("decision")
    checklist_ref = modules.get(module_name, {}).get("checklist")

    return decision, checklist_ref


# reserve for landing page
@app.route('/', methods=['GET'])
def homepage():
    return render_template("landing.html", data=sorted(module_descriptions, key=lambda k: k["moduleName"]))


@app.route('/error', methods=['GET'])
def error():
    return render_template("error.html")


@app.route('/about-us', methods=['GET'])
def about():
    return render_template("about-us.html")


@app.route('/<module_name>/questions', methods=['GET'])
def questions(module_name):
    return render_template('questions.html', data=sorted(module_descriptions, key=lambda k: k["moduleName"]))


@app.route('/<module_name>/questions', methods=['POST'])
def update_questions(module_name):
    if request.get_json() and request.get_json()['QID'] and 'qna' in request.get_json().keys():
        past_qna = request.get_json()['qna']
        question_id = request.get_json()['QID']

        decision, checklist_ref = _populate(module_name)
        if decision is None or checklist_ref is None:
            abort(404, "Module does not exist!")

        if question_id != "null":
            page = decision.get_current_page(question_id)
            min_num_q = decision.min_num_q
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


@app.route('/<module_name>/next', methods=['POST'])
def next_question(module_name):
    if request.get_json() and request.get_json()['QID'] and request.get_json()['AID'] \
            and 'qna' in request.get_json().keys():
        past_qna = request.get_json()['qna']
        question_id = request.get_json()['QID']
        answer_id_list = request.get_json()['AID']

        # add current question and answer to the past qna list for further critera
        if {"QID": question_id, "AID": answer_id_list} not in past_qna:
            past_qna.insert(0, {"QID": question_id, "AID": answer_id_list})

        decision, checklist_ref = _populate(module_name)
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
                "checklist": checklist
            }
    else:
        abort(403, 'Incomplete question id and answer id!')


@app.route('/<module_name>/prev', methods=['POST'])
def prev_question(module_name):
    if request.get_json() and request.get_json()['prevQID']:
        prev_question_id = request.get_json()['prevQID']
        decision, checklist_ref = _populate(module_name)
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
