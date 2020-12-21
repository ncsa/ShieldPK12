from flask import Flask, render_template, request, abort, redirect, url_for

from testing_decision_tree import Testing_Decision_Tree

app = Flask(__name__)

# initialize the tree
testing_decision_tree = Testing_Decision_Tree()


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
    return {
        "root_nid": testing_decision_tree.tree.root,
        "current_node": vars(testing_decision_tree.tree.get_node(current_nid)),
        "option_nodes": [vars(node) for node in option_nodes]
    }


@app.route('/next', methods=['POST'])
def next():
    if request.get_json() and request.get_json()['selected_nid']:
        selected_nid = int(request.get_json()['selected_nid'])
        option_nodes = testing_decision_tree.tree.children((selected_nid))
        return {
            "root_nid": testing_decision_tree.tree.root,
            "current_node": vars(testing_decision_tree.tree.get_node(selected_nid)),
            "option_nodes": [vars(node) for node in option_nodes]
        }
    else:
        abort(403, 'need to provide the selected identifier')


@app.route('/prev', methods=['POST'])
def prev():
    if request.get_json() and request.get_json()['current_nid']:
        current_nid = int(request.get_json()['current_nid'])
        current = testing_decision_tree.tree.get_node(current_nid)
        option_nodes = testing_decision_tree.tree.children((current.bpointer))
        return {
            "root_nid": testing_decision_tree.tree.root,
            "current_node": vars(testing_decision_tree.tree.get_node(current.bpointer)),
            "option_nodes": [vars(node) for node in option_nodes]
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
            past_nodes.insert(0, vars(testing_decision_tree.tree.get_node(nid)))
        return {
            "root_nid": testing_decision_tree.tree.root,
            "current_node": vars(testing_decision_tree.tree.get_node(submitted_nid)),
            "past_nodes": past_nodes
        }
    else:
        abort(403, 'need to provide the submitted identifier')