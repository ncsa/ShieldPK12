from treelib import Node, Tree


class Testing_Decision_Tree:

    def __init__(self):
        # read from json and auto populate a tree
        self.tree = Tree()
        self.tree.create_node(tag="Will You Test", identifier=1)  # root node

        self.tree.create_node("Required?", 2, parent=1)
        self.tree.create_node("Who?", 3, parent=1)
        self.tree.create_node("Where?", 4, parent=1)
        self.tree.create_node("How often?", 5, parent=1)
        self.tree.create_node("How to share results?", 6, parent=1)
        self.tree.create_node("Which test?", 7, parent=1)

        self.tree.create_node("Mandatory", 8, parent=2)
        self.tree.create_node("Voluntary", 9, parent=2)
        self.tree.create_node("all", 10, parent=8)
        self.tree.create_node("In-person only?", 11, parent=8)
        self.tree.create_node("Expected number?", 12, parent=9)

        self.tree.create_node("All", 13, parent=3)
        self.tree.create_node("Adults", 14, parent=3)
        self.tree.create_node("Random sample", 15, parent=3)
        self.tree.create_node("High risk (sports)", 16, parent=3)

        self.tree.create_node("At home", 17, parent=4)
        self.tree.create_node("In person", 18, parent=4)
        self.tree.create_node("Collection kits", 19, parent=17)
        self.tree.create_node("Chain of Custody", 20, parent=17)
        self.tree.create_node("How to return", 21, parent=17)
        self.tree.create_node("Weekly supply", 22, parent=19)
        self.tree.create_node("Quarterly supply", 23, parent=19)

        self.tree.create_node("Timing", 24, parent=18)
        self.tree.create_node("Where", 25, parent=18)
        self.tree.create_node("In class", 26, parent=25)
        self.tree.create_node("Testing center", 27, parent=25)
        self.tree.create_node("Sample movement", 28, parent=26)
        self.tree.create_node("Traffic flow", 29, parent=27)

        self.tree.create_node("Parents", 30, parent=6)
        self.tree.create_node("Public Health", 31, parent=6)
        self.tree.create_node("Community", 32, parent=6)
        self.tree.create_node("Close contacts", 33, parent=6)

        self.tree.create_node("Sample type", 34, parent=7)
        self.tree.create_node("Speed of results", 35, parent=7)
        self.tree.create_node("cost", 36, parent=7)

if __name__ == "__main__":
    testing_decision_tree = Testing_Decision_Tree()
    testing_decision_tree.tree.show()

    # get node given id
    current = testing_decision_tree.tree.get_node(25)
    print("current:", vars(current))

    # check if it's the end
    print("is the end:", current.is_leaf())

    # list all the options
    options_pointers= current.fpointer
    print(testing_decision_tree.tree.children(25))

    # going back to last step
    print(testing_decision_tree.tree.children(current.bpointer))

    print(testing_decision_tree.tree.root)