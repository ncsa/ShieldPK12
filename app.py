from flask import Flask, render_template, request, abort, send_file, send_from_directory
import zipfile
from testing_decision_tree import Testing_Decision_Tree
import os
import io
import time

app = Flask(__name__)

# initialize the tree
testing_decision_tree = Testing_Decision_Tree()

# resource folder name
resource_foldername = "resources"

@app.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html')


@app.route('/questions', methods=['GET'])
def questions():
    return render_template('questions.html')


@app.route('/questions', methods=['POST'])
def update_questions():
    current_nid = request.get_json()['current_nid']
    # if not given then default to root
    if not current_nid:
        current_nid = testing_decision_tree.tree.root
    else:
        current_nid = int(current_nid)

    option_nodes = testing_decision_tree.tree.children(current_nid)
    option_nodes_dict =[]
    for node in option_nodes:
        temp = _node_to_dict(node)
        option_nodes_dict.append(temp)
    return {
        "root_nid": testing_decision_tree.tree.root,
        "current_node": _node_to_dict(testing_decision_tree.tree.get_node(current_nid)),
        "option_nodes": option_nodes_dict
    }


@app.route('/next', methods=['POST'])
def next():
    if request.get_json() and request.get_json()['selected_nid']:
        selected_nid = int(request.get_json()['selected_nid'])
        option_nodes = testing_decision_tree.tree.children((selected_nid))
        option_nodes_dict = []
        for node in option_nodes:
            temp = _node_to_dict(node)
            option_nodes_dict.append(temp)
        return {
            "root_nid": testing_decision_tree.tree.root,
            "current_node": _node_to_dict(testing_decision_tree.tree.get_node(selected_nid)),
            "option_nodes": option_nodes_dict
        }
    else:
        abort(403, 'need to provide the selected identifier')


@app.route('/prev', methods=['POST'])
def prev():
    if request.get_json() and request.get_json()['current_nid']:
        current_nid = int(request.get_json()['current_nid'])
        current = testing_decision_tree.tree.get_node(current_nid)
        option_nodes = testing_decision_tree.tree.children((current.bpointer))
        option_nodes_dict = []
        for node in option_nodes:
            temp = _node_to_dict(node)
            option_nodes_dict.append(temp)
        return {
            "root_nid": testing_decision_tree.tree.root,
            "current_node": _node_to_dict(testing_decision_tree.tree.get_node(current.bpointer)),
            "option_nodes": option_nodes_dict
        }
    else:
        abort(403, 'need to provide the current identifier')


@app.route("/submit", methods=['POST'])
def submit():
    if request.get_json() and request.get_json()['submitted_nid']:
        submitted_nid = int(request.get_json()['submitted_nid'])
        past_nodes = []
        for nid in testing_decision_tree.tree.rsearch(submitted_nid):
            # flip the order of nodes; parent - child
            past_nodes.insert(0, _node_to_dict(testing_decision_tree.tree.get_node(nid)))
        return {
            "root_nid": testing_decision_tree.tree.root,
            "current_node": _node_to_dict(testing_decision_tree.tree.get_node(submitted_nid)),
            "past_nodes": past_nodes
        }
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
        return send_file(memory_file, attachment_filename='resources.zip',
                         as_attachment=True)
    else:
        abort(403, "You need to provide a list of filenames to download!")


def _node_to_dict(node):
    temp = {
        "tag":node.tag,
        "identifier":node.identifier,
        "data": vars(node.data)
    }

    return temp