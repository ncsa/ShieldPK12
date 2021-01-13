import json

class Module:

    def __init__(self, json_fname):
        with open(json_fname, "r") as f:
            self.module = json.load(f)

    def get_current_page(self, question_id="1"):
        for page in self.module:
            if page["QID"] == question_id:
                return page
        raise ValueError("current page id: " + question_id + " cannot be found!")

    def next_page(self, question_id, answer_id_list):
        next_page_id = None
        current_page = None
        current_answer = None
        for page in self.module:
            if page["QID"] == question_id:
                current_page = page

                for answer in page["answers"]:
                    # assume all the multiple choice will lead to the same next question; hence use the first answer
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
                    return page
            raise ValueError("Next page id: " + next_page_id + " cannot be found!")
        else:
            # reach the end
            return None

    def prev_page(self, prev_question_id):
        if prev_question_id:
            for page in self.module:
                if page["QID"] == prev_question_id:
                    return page
            raise ValueError("Previous page id: " + prev_question_id + " cannot be found!")
        else:
            # reach the beginning
            return None

    def get_all_past_questions_answers(self, pastQNA):
        """
        given question and answer map get their details
        :param pastQNA: [{ "QID": xxx, "AID":[xxx, xxx, ...]}, ...]
        :return:
        """
        response = []
        for qna in pastQNA:

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
                                "answer": answer["answer"],
                                "description": answer["description"],
                                "answerResources": answer["resources"]
                            })

                    response.append({
                        "QID": page["QID"],
                        "question": page["question"],
                        "questionDescription": page["description"],
                        "questionResources": page["resources"],
                        "answers": answer_list
                    })

                    if not found_answer:
                        raise ValueError("AID: " + qna["AID"] + "not found!")

            if not found_page:
                raise ValueError("QID: " + qna["QID"] + " not found!")

        return response


if __name__ == "__main__":
   testing_decision_module = Module("decisiontrees/testing_decision.json")
   print(testing_decision_module.get_current_page("7d"))
   print(testing_decision_module.next_page(question_id="2", answer_id_list=["2b"]))
   print(testing_decision_module.prev_page(prev_question_id="7c"))
   print(testing_decision_module.get_all_past_questions_answers([{"QID":"2","AID":["2c"]},{"QID":"1","AID":["1a"]}]))
