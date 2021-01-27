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
            module = json.load(f)

            for page in module:
                for answer in page["answers"]:
                    if answer["answer"] == "":
                        print("Module:", json_fname.split("/")[1].split(".")[0].split("_")[0].upper())
                        print(page["QID"])
                        print(page["question"])
                        print("\n")
                        break

