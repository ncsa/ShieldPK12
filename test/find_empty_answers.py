import json


if __name__ == "__main__":
    decision_fnames = [
        "decisiontrees/cleaning/cleaning_decision.json",
        "decisiontrees/distancing/distancing_decision.json",
        "decisiontrees/mask/mask_decision.json",
        "decisiontrees/testing/testing_decision.json",
        "decisiontrees/ventilation/ventilation_decision.json",
        "decisiontrees/data-infrastructure/IT_decision.json"
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

