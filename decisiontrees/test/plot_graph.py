import networkx as nx
import matplotlib.pyplot as plt
import json


if __name__ == "__main__":
    decision_fnames = [
        "../cleaning_decision.json",
        "../distancing_decision.json",
        "../mask_decision.json",
        "../testing_decision.json",
        "../ventilation_decision.json",
        # "../IT_decision.json"
    ]
    for json_fname in decision_fnames:
        with open(json_fname, "r") as f:
            module_name = json_fname.split("/")[1][:-5]
            G = nx.DiGraph()
            module = json.load(f)

            for page in module:
                G.add_node(page["QID"], text=page["question"])
                for answer in page["answers"]:
                    if answer["nextQID"] is not None:
                        G.add_edge(page["QID"], answer["nextQID"])


            plt.figure(figsize=(14, 11))
            plt.title(module_name.upper().replace("_", " "))

            labels = nx.get_node_attributes(G, 'text')
            pos_nodes = nx.circular_layout(G)
            pos_attrs = {}
            for node, coords in pos_nodes.items():
                pos_attrs[node] = (coords[0], coords[1] + 0.08)
            nx.draw(G, pos_nodes, node_size=1000, with_labels=True)
            nx.draw_networkx_labels(G, pos_attrs, labels=labels, font_size=8)

            plt.savefig(module_name + "_graph.png")

