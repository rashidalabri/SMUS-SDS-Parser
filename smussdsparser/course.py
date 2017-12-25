from .session import Session
import bs4
import datetime
from .assignment import Assignment
from .assignment_mark import AssignmentMark


class Course:

    def __init__(self, session, course_id):
        self.session = session
        self.course_id = course_id

        course_information = self.get_course_information()

        self.course_name = course_information['course_name']
        self.teacher_name = course_information['teacher_name']
        self.has_lessons = course_information['has_lessons']
        self.has_assignments = course_information['has_assignments']
        self.has_assignment_marks = course_information['has_assignment_marks']

    def get_course_information(self):
        course_information = {}
        r = self.session.get(Session.BASE_URL, self.append_course_id_to_params('course_summary'))
        page = bs4.BeautifulSoup(r.text, 'lxml')
        course_information['course_name'] = page.select('h1')[0].text.strip().lstrip().replace(' summary', '')
        course_information['teacher_name'] = page.select('#content')[0].find_all('a')[-1].text.replace('(', '').replace(')', '')
        course_information['has_lessons'] = 'Lessons' in page.text
        course_information['has_assignments'] = 'Assignments' in page.text
        course_information['has_assignment_marks'] = 'Assignment marks' in page.text
        return course_information

    def append_course_id_to_params(self, param_name):
        params = dict(Session.PAGE_PARAMS[param_name])
        params['course_id'] = self.course_id
        return params

    def get_assignments(self):
        assignments = []
        if not self.has_assignments:
            return assignments
        r = self.session.get(Session.BASE_URL, params=self.append_course_id_to_params('course_assignments'))
        page = bs4.BeautifulSoup(r.text, 'lxml')
        rows = page.select('#content')[0].select('table')[0].find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('td')
            assignments.append(Assignment(
                assignment_number=cells[0].text.strip().lstrip(),
                assignment_type=cells[1].text.strip().lstrip(),
                title=cells[2].text.strip().lstrip(),
                description=cells[3].text.strip().lstrip(),
                due_date=datetime.datetime.strptime(cells[4].text.strip().lstrip(), '%A %d %B, %Y').date(),
                max_mark=cells[5].text.strip().lstrip(),
            ))
        return assignments

    def get_assignments(self):
        assignments = []
        if not self.has_assignments:
            return assignments
        r = self.session.get(Session.BASE_URL, params=self.append_course_id_to_params('course_assignments'))
        page = bs4.BeautifulSoup(r.text, 'lxml')
        rows = page.select('#content')[0].select('table')[0].find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('td')
            assignments.append(Assignment(
                assignment_number=cells[0].text.strip().lstrip(),
                assignment_type=cells[1].text.strip().lstrip(),
                title=cells[2].text.strip().lstrip(),
                description=cells[3].text.strip().lstrip(),
                due_date=datetime.datetime.strptime(cells[4].text.strip().lstrip(), '%A %d %B, %Y').date(),
                max_mark=cells[5].text.strip().lstrip(),
            ))
        return assignments

    def get_assignment_marks(self):
        assignment_marks = []
        if not self.has_assignment_marks:
            return assignment_marks
        r = self.session.get(Session.BASE_URL, params=self.append_course_id_to_params('course_assignment_marks'))
        page = bs4.BeautifulSoup(r.text, 'lxml')
        rows = page.select('#content')[0].select('table')[0].find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('td')
            assignment_marks.append(AssignmentMark(
                assignment_type=cells[0].text.strip().lstrip(),
                title=cells[1].text.strip().lstrip(),
                date_submitted=cells[2].text.strip().lstrip(),
                mark=cells[3].text.strip().lstrip(),
                percent=cells[4].text.strip().lstrip(),
                percentage_of_total=cells[5].text.strip().lstrip()
            ))
        return assignment_marks

    def __str__(self):
        return self.course_name + ' - ' + self.teacher_name

    def __repr__(self):
        return self.__str__()
