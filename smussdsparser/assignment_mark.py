class AssignmentMark:

    def __init__(self, assignment_type=None, title=None, date_submitted=None, mark=None, percent=None, percentage_of_total=None):
        self.assignment_type = assignment_type
        self.title = title
        self.date_submitted = date_submitted
        self.mark = mark
        self.percent = percent
        self.percentage_of_total = percentage_of_total

    def __str__(self):
        return str(self.title) + ' - ' + str(self.percent)

    def __repr__(self):
        return self.__str__()
