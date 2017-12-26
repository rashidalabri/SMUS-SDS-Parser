import bs4
import datetime
import re
from .session import Session
from .course import Course


class Student:

    def __init__(self, session):
        self.session = session

        student_information = self.get_student_information()

        self.name = student_information['student_name']
        self.grade = int(student_information['grade'])
        self.birth_date = datetime.datetime.strptime(student_information['birthdate'], '%d %B, %Y').date()
        self.house = student_information['house']
        self.competitive_house = student_information['competitive_house']
        self.day_student = student_information['day_student?']
        self.PEN = int(student_information['pen'])
        self.AP_number = student_information['ap_number']
        self.student_number = int(student_information['student_number'])
        self.enrolment_date = datetime.datetime.strptime(student_information['enrolment_date'], '%d %B, %Y').date()
        self.finish_date = datetime.datetime.strptime(student_information['finish_date'], '%d %B, %Y').date()
        self.allergies = student_information['allergies']
        self.health_card_number = int(student_information['health_card_number'].replace(' ', ''))
        self.citizenship = student_information['citizenship']

        self.courses = self.get_student_courses()

    def get_student_information(self):
        """
        Returns student information by fetching the student information page and parsing the information table
        """
        r = self.session.get(Session.BASE_URL, params=Session.PAGE_PARAMS['student_information'])
        page = bs4.BeautifulSoup(r.text, 'lxml')
        tables = page.find_all('table')
        student_information = {}
        for row in tables[1].find_all('tr'):
            cells = row.find_all('td')
            name = cells[0].text.lstrip().strip().lower().replace(' ', '_')
            value = cells[1].text.lstrip().strip()
            student_information[name] = value
        return student_information

    def get_student_courses(self):
        """
        Returns the courses the student is currently enrolled in by fetching menu items from the RPC and parsing them.
        The RPC menu item retriever works on a toggle basis, which is my a while loop is necessary.
        """
        r = self.session.get(Session.RPC_URL, params=Session.RPC_PARAMS['student_menu'])
        while True:
            if 'course_summary.php' in r.text:
                break
            r = self.session.get(Session.RPC_URL, params=Session.RPC_PARAMS['student_menu'])

        page = bs4.BeautifulSoup(r.text, 'lxml')
        student_courses = []
        for course in page.select('#newmenu3')[0].find_all('a', href=True):
            course_id = re.sub('[^0-9]', '', course['href'])
            student_courses.append(Course(self.session, course_id))
        return student_courses
