import json


if __name__ == "__main__":
    resources = [
        "../decisiontrees/cleaning_decision.json",
        "../decisiontrees/distancing_decision.json",
        "../decisiontrees/mask_decision.json",
        "../decisiontrees/testing_decision.json",
        "../decisiontrees/ventilation_decision.json",
        "../decisiontrees/data-infrastructure_decision.json",
        "../decisiontrees/vaccine_decision.json"
    ]
    for module in resources:
        with open(module, "r") as f:
            module_config = json.load(f)
            decision = module_config["moduleContent"]
            checklist = module_config["checklist"]

            activityID = 0
            for activity in checklist:
                # sequentially assign activity ID
                # activityID += 1
                # activity["activityID"] = str(activityID)


                # check if answer ID exists
                if activity["rules"]["operator"] != "ALL":
                    for entry in activity["rules"]["criteria"]:
                        found = False
                        for page in decision:
                            for answer in page["answers"]:
                                if entry["AID"] == answer["AID"]:
                                    found = True
                        if not found:
                            print("module:", module,
                                  "activityID:", activity["activityID"],
                                  "AID: ", entry["AID"])
            # f.seek(0)
            # json.dump(module_config, f, indent=2)


