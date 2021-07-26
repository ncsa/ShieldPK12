import json


if __name__ == "__main__":
    decision_fnames = [
        "../decisiontrees/cleaning_decision.json",
        "../decisiontrees/distancing_decision.json",
        "../decisiontrees/mask_decision.json",
        "../decisiontrees/testing_decision.json",
        "../decisiontrees/ventilation_decision.json",
        "../decisiontrees/data-infrastructure_decision.json",
        "../decisiontrees/vaccine_decision.json",
        "../decisiontrees/special_education_decision.json"
    ]
    for json_fname in decision_fnames:
        with open(json_fname, "r") as f:
            module = json.load(f)["moduleContent"]

            for page in module:
                for answer in page["answers"]:
                    if answer["answer"] == "":
                        print("Module:", json_fname.split("/")[1].split(".")[0].split("_")[0].upper())
                        print(page["QID"])
                        print(page["question"])
                        print("\n")
                        break

