import requests
import bs4
from .notloggedinexception import NotLoggedInException


class Session:

    BASE_URL = 'https://sds.smus.ca/index.php'

    PAGE_PARAMS = {
        'login': {'next_page': 'login.php'},
        'student_information': {'next_page': 'student_sds/student_information.php'},
        'course_summary': {'next_page': 'student_sds/course_summary.php', 'course_id': ''},
        'course_assignments': {'next_page': 'student_sds/course_assignments.php', 'course_id': ''},
        'course_assignment_marks': {'next_page': 'student_sds/course_assignment_marks.php', 'course_id': ''}
    }

    RPC_URL = 'https://sds.smus.ca/rpc.php'

    RPC_PARAMS = {
        'student_menu': {'action': 'modern_menu', 'level': '1', 'id': 'Student Menu'},
        'my_courses': {'action': 'modern_menu', 'level': '2', 'id': 'My Courses'}
    }

    def __init__(self, session_id=None, username=None, password=None):
        if session_id is not None:
            self.cookie_jar = dict(PHPSESSID=session_id)
        elif username is not None and password is not None:
            self.cookie_jar = self.get_logged_in_cookie_jar(username, password)
        else:
            self.cookie_jar = dict()

    def get_logged_in_cookie_jar(self, username, password):
        r = requests.get(self.BASE_URL, params=self.PAGE_PARAMS['login'])
        cookie_jar = r.cookies
        page = bs4.BeautifulSoup(r.text, 'lxml')
        csrf_token = page.select('input[name=CSRFtoken]')[0]['value']
        r = requests.post(self.BASE_URL, cookies=cookie_jar, data={
            'user_name': username,
            'password': password,
            'CSRFtoken': csrf_token,
            'next_page': 'login.php',
            'validator': 'login.php'
        })
        print(r.text)
        return cookie_jar

    def is_logged_in(self):
        r = self.get(self.BASE_URL, ignore_logged_in=True)
        return 'You are:' in r.text

    def get(self, url, params=None, ignore_logged_in=False):
        if (not ignore_logged_in) and (not self.is_logged_in()):
            raise NotLoggedInException
        return requests.get(url, params=params, cookies=self.cookie_jar)

    def post(self, url, data=None, params=None, ignore_logged_in=False):
        if (not ignore_logged_in) and (not self.is_logged_in()):
            raise NotLoggedInException
        return requests.get(url, data=data, params=params, cookies=self.cookie_jar)
