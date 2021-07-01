import json


if __name__ == "__main__":
    resources = [
        {
            "decision":"../cleaning_decision.json",
            "checklist":"../cleaning_checklist.json"
        },
        {
            "decision": "../distancing_decision.json",
            "checklist": "../distancing_checklist.json"
        },
        {
            "decision":"../mask_decision.json",
            "checklist": "../mask_checklist.json"
        },
        {
            "decision": "../IT_decision.json",
            "checklist": "../IT_checklist.json"
        },
        {
            "decision": "../testing_decision.json",
            "checklist": "../testing_checklist.json"
        },
        {
            "decision": "../ventilation_decision.json",
            "checklist": "../ventilation_checklist.json"
        },
    ]

    for module in resources:
        with open(module['decision'], "r") as f:
            decision = json.load(f)

            with open(module['checklist'], "r+") as c:
                checklist = json.load(c)

                activityID = 0
                for activity in checklist:
                    # sequentially assign activity ID
                    activityID += 1
                    activity["activityID"] = str(activityID)


                    # check if answer ID exists
                    if activity["rules"]["operator"] != "ALL":
                        for entry in activity["rules"]["criteria"]:
                            found = False
                            for page in decision:
                                for answer in page["answers"]:
                                    if entry["AID"] == answer["AID"]:
                                        found = True
                            if not found:
                                print("module:", module['checklist'],
                                      "activityID:", activity["activityID"],
                                      "AID: ", entry["AID"])
                c.seek(0)
                json.dump(checklist, c, indent=2)


