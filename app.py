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
    current_nid = request.args.get('current_nid')

    # if not given then default to root
    if not current_nid:
        current_nid = testing_decision_tree.tree.root

    option_nodes = testing_decision_tree.tree.children(int(current_nid))
    return render_template('questions.html', current_nid=current_nid, option_nodes=[vars(node) for node in option_nodes])


@app.route('/next', methods=['POST'])
def next():
    if request.get_json() and request.get_json()['selected_nid']:
        selected_nid = request.get_json()['selected_nid']
        return redirect(url_for("questions", current_nid=selected_nid))
    else:
        abort(403, 'need to provide the selected identifier')


@app.route('/prev', methods=['POST'])
def prev():
    if request.get_json() and request.get_json()['current_nid']:
        current_nid = request.get_json()['current_nid']
        current = testing_decision_tree.tree.get_node(current_nid)
        return redirect(url_for("questions", current_nid=current.bpointer))
    else:
        abort(403, 'need to provide the current identifier')
