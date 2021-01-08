from flask import Flask, render_template, request, abort, send_file, send_from_directory
import zipfile
from decisiontrees.module import Module
import os
import io
import time

app = Flask(__name__)

# initialize the module
# TODO put the path in a config file
testing_decision = Module("decisiontrees/testing_decision.json")
resource_foldername = "resources"

@app.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html')


@app.route('/questions', methods=['GET'])
def questions():
    return render_template('questions.html')


@app.route('/questions', methods=['POST'])
def update_questions():
    question_id = request.get_json()['questionID']
    page = testing_decision.get_current_page(question_id)

    return page


@app.route('/next', methods=['POST'])
def next_question():
    if request.get_json() and request.get_json()['questionID'] and request.get_json()['answerID']:
        question_id = request.get_json()['questionID']
        answer_id = request.get_json()['answerID']
        return testing_decision.next_page(question_id, answer_id)
    else:
        abort(403, 'Incomplete question id and answer id!')


@app.route('/prev', methods=['POST'])
def prev_question():
    if request.get_json() and request.get_json()['prevQuestionID']:
        question_id = request.get_json()['prevQuestionID']
        return testing_decision.prev_page(question_id)
    else:
        abort(403, 'need to provide the correct previous question id!')


@app.route("/submit", methods=['POST'])
def submit():
    if request.get_json() and request.get_json()['qna']:
        questions_n_answers = request.get_json()['qna']
        return testing_decision.get_all_past_questions_answers(questions_n_answers)
    else:
        abort(403, 'need to provide the submitted identifier')


@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    resources_path = os.path.join(app.static_folder, resource_foldername)
    try:
        return send_from_directory(directory=resources_path, filename=filename)
    except FileNotFoundError:
        abort(404, "file not found")


@app.route("/download-zip", methods=['POST'])
def download_list_of_files():
    if request.get_json() and request.get_json()['filename_list']:
        filename_list = request.get_json()['filename_list']
        resources_path = os.path.join(app.static_folder, resource_foldername)
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for filename in filename_list:
                # check if file exist in the resources folder
                if os.path.isfile(os.path.join(resources_path, filename)):
                    data = zipfile.ZipInfo(filename)
                    data.date_time = time.localtime(time.time())[:6]
                    data.compress_type = zipfile.ZIP_DEFLATED
                    zf.write(os.path.join(resources_path, filename),
                             arcname=os.path.join(resource_foldername, filename))
        memory_file.seek(0)
        return send_file(memory_file, attachment_filename='resources.zip')
    else:
        abort(403, "You need to provide a list of filenames to download!")