import json

class Module:

    def __init__(self, json_fname):
        with open(json_fname, "r") as f:
            self.module = json.load(f)

    def get_current_page(self, question_id="1"):
        for page in self.module:
            if page["questionID"] == question_id:
                return page
        raise ValueError("current page id: " + question_id + " cannot be found!")

    def next_page(self, question_id, answer_id):
        next_page_id = None
        current_page = None
        current_answer = None
        for page in self.module:
            if page["questionID"] == question_id:
                current_page = page

                for answer in page["answers"]:
                    if answer["answerID"] == answer_id:
                        current_answer = answer
                        next_page_id = answer["nextQuestionID"]
                        break
                    break
                if current_answer is None:
                    raise ValueError("Current answer id: " + answer_id + " cannot be found!")

        if current_page is None:
            raise ValueError("Current page id: " + question_id + " cannot be found!")

        if next_page_id:
            for page in self.module:
                if page["questionID"] == next_page_id:
                    return page
            raise ValueError("Next page id: " + next_page_id + " cannot be found!")
        else:
            # reach the end
            return None

    def prev_page(self, question_id):
        prev_page_id = None
        current_page = None
        for page in self.module:
            if page["questionID"] == question_id:
                current_page = page
                prev_page_id = page["prevQuestionID"]
                break

        if current_page is None:
            raise ValueError("Current page id: " + question_id + " cannot be found!")

        if prev_page_id:
            for page in self.module:
                if page["questionID"] == prev_page_id:
                    return page
            raise ValueError("Previous page id: " + prev_page_id + " cannot be found!")
        else:
            # reach the beginning
            return None

    def get_all_past_questions_answers(self, qa_map):
        """
        given question and answer map get their details
        :param qa_map: { questionID: answerID }
        :return:
        """
        response = []
        for question_id, answer_id in qa_map.items():
            found_page = False
            for page in self.module:

                if page["questionID"] == question_id:
                    found_page = True

                    found_answer = False
                    for answer in page["answers"]:

                        if answer["answerID"] == answer_id:
                            found_answer = True
                            response.append({
                                "question": page["question"],
                                "questionDescription": page["description"],
                                "questionResources": page["resources"],
                                "answer": answer["answer"],
                                "answerDescription": answer["description"],
                                "answerResources": page["resources"]
                            })
                    if not found_answer:
                        raise ValueError("answerID: " + answer_id + "not found!")

            if not found_page:
                raise ValueError("questionID: " + question_id + " not found!")

        return response


if __name__ == "__main__":
   testing_decision_module = Module("decisiontrees/testing_decision.json")
   print(testing_decision_module.get_current_page("7d"))
   print(testing_decision_module.next_page(question_id="7d", answer_id="7d-i"))
   print(testing_decision_module.prev_page(question_id="7a"))
