class Assignment:

    def __init__(self, assignment_number=None, assignment_type=None, title=None, description=None, due_date=None, max_mark=None):
        self.assignment_number = assignment_number
        self.assignment_type = assignment_type
        self.title = title
        self.description = description
        self.due_date = due_date
        self.max_mark = max_mark

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return self.__str__()