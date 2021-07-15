import json

class Module:

    def __init__(self, module):
        self.module = module
        self.max_num_q = len(self.module)
        self.min_num_q = len([m for m in self.module if "rules" not in m ])

    def get_current_page(self, question_id="1"):
        for page in self.module:
            if page["QID"] == question_id:
                return page
        raise ValueError("current page id: " + question_id + " cannot be found!")

    def next_page(self, question_id, answer_id_list, past_qna):
        next_page_id = None
        current_page = None
        current_answer = None

        for page in self.module:
            if page["QID"] == question_id:

                current_page = page
                for answer in page["answers"]:
                    # if multiple answer, start with the first one
                    if answer["AID"] == answer_id_list[0]:
                        current_answer = answer
                        next_page_id = answer["nextQID"]
                        break

                if current_answer is None:
                    raise ValueError("Current answer id: " + answer_id_list[0] + " cannot be found!")

        if current_page is None:
            raise ValueError("Current page id: " + question_id + " cannot be found!")

        if next_page_id:
            for page in self.module:
                if page["QID"] == next_page_id:
                    # here need to check if the next page has skip rules recursively
                    return self._skip_page(page, past_qna)
            raise ValueError("Next page id: " + next_page_id + " cannot be found!")
        else:
            # reach the end
            return None

    def _skip_page(self, page, past_qna):
        if "rules" in page.keys():
            past_answers_list = self._flatten_answers(past_qna)
            if page["rules"].get("operator") == "AND":
                match = True
                for criterion in page["rules"]["criteria"]:
                    if criterion["AID"] not in past_answers_list:
                        match = False
                if not match:
                    # skip this question and go to the next
                    return self.next_page(question_id=page["QID"],
                                          answer_id_list=[page["answers"][-1]["AID"]],
                                          past_qna=past_qna)
                else:
                    return page
        return page

    def prev_page(self, prev_question_id):
        if prev_question_id:
            for page in self.module:
                if page["QID"] == prev_question_id:
                    return page
            raise ValueError("Previous page id: " + prev_question_id + " cannot be found!")
        else:
            # reach the beginning
            return None

    def generate_qna_report(self, past_qna):
        """
        given question and answer map get their details
        :param past_qna: [{ "QID": xxx, "AID":[xxx, xxx, ...]}, ...]
        :return:
        """
        response = []

        # reverse the order so correct report order can be generated
        past_qna.reverse()
        for qna in past_qna:

            found_page = False
            for page in self.module:

                if page["QID"] == qna["QID"]:
                    found_page = True

                    found_answer = False
                    answer_list = []
                    for answer in page["answers"]:
                        if answer["AID"] in qna["AID"]:
                            found_answer = True
                            answer_list.append({
                                "AID": answer["AID"],
                                "prettyAID": answer.get("prettyAID"),
                                "answer": answer["answer"],
                                "description": answer["description"],
                                "resources": answer["resources"]
                            })

                    response.append({
                        "QID": page["QID"],
                        "question": page["question"],
                        "description": page["description"],
                        "resources": page["resources"],
                        "answers": answer_list
                    })

                    if not found_answer:
                        raise ValueError("AID: " + qna["AID"] + "not found!")

            if not found_page:
                raise ValueError("QID: " + qna["QID"] + " not found!")

        return response

    def compile_checklist(self, past_qna, reference: dict):
        """
        given question and answer map get their checklist
        can be connected with generate_qna_report
        :param past_qna:
        :param reference: [{"activity":..}]
        :return:
        """
        answer_id_list = self._flatten_answers(past_qna)
        checklist = []
        for reference_item in reference:
            operator = reference_item["rules"]["operator"]

            if operator == "AND":
                match = True
                for criterion in reference_item["rules"]["criteria"]:
                    if criterion["AID"] not in answer_id_list:
                        match = False
                if match:
                    checklist.append(reference_item)

            elif operator == "OR":
                match = False
                for criterion in reference_item["rules"]["criteria"]:
                    if criterion["AID"] in answer_id_list:
                        match = True
                if match:
                    checklist.append(reference_item)

            elif operator == "NOT":
                raise ValueError("Not rules not implemented yet!")

            elif operator == "ALL":
                checklist.append(reference_item)

            else:
                raise ValueError(operator + "rules not implemented yet!")

        return checklist

    @staticmethod
    def _flatten_answers(past_qna):
        answer_id_list = []
        for qna in past_qna:
            for id in qna["AID"]:
                answer_id_list.append(id)

        return answer_id_list

if __name__ == "__main__":
    distancing_decision_module = Module("decisiontrees/distancing_decision.json")
    with open("decisiontrees/distancing_checklist.json", "r") as f:
        ref = json.load(f)
    past_qna = [{"QID": "4b", "AID": ["4b-iv"]}, {"QID": "4", "AID": ["4b", "4c"]}, {"QID": "3c", "AID": ["3c-i"]},
                {"QID": "3b", "AID": ["3b-iv-1"]}, {"QID": "3", "AID": ["3b", "3c"]},
                {"QID": "2b-ii", "AID": ["2b-ii-1"]}, {"QID": "2b-i", "AID": ["2b-i-3"]}, {"QID": "2b", "AID": ["2b"]},
                {"QID": "2a-ii-3", "AID": ["2a-ii-3-b"]}, {"QID": "2a-ii-2", "AID": ["2a-ii-2"]},
                {"QID": "2a-ii-1", "AID": ["2a-ii-1-a"]}, {"QID": "2a", "AID": ["2a-ii"]}, {"QID": "2", "AID": ["2"]},
                {"QID": "1c", "AID": ["1c-yes"]}, {"QID": "1b", "AID": ["1b-i"]}, {"QID": "1a", "AID": ["1a-i"]},
                {"QID": "1", "AID": ["1"]}]
    # print(distancing_decision_module.next_page(question_id="3", answer_id_list=["3a", "3c"], past_qna=past_qna))
    report = distancing_decision_module.generate_qna_report(past_qna)
    print(report)
    # checklist = distancing_decision_module.compile_checklist(past_qna, ref)
    # print(checklist)
