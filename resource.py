
class Resource:
    def __init__(self, answer_type="single", explanation="", file_list=[]):
        self.answer_type = answer_type
        self.file_list = file_list
        self.explanation = explanation
        # TODO add more useful information on each node