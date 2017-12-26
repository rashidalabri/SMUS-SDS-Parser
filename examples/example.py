import smussdsparser

# The session_id can be obtained by logging into SMUS SDS and using a chrome extension like EditThisCookie to find
# the PHPSESSID cookie value.
session_id = 'aaaaaaaaaaaaaaaaaaaaaaaa'

# The first step is creating our session
my_session = smussdsparser.Session(session_id)

# We create a student object by passing our session to the Student class
try:
    my_account = smussdsparser.Student(my_session)
except smussdsparser.NotLoggedInException:
    print('The session is not logged in.')
    exit()

# Student objects have many attributes including name and courses
print('Welcome ' + my_account.name + '.')
print('You are currently enrolled in ' + str(len(my_account.courses)) + ' courses.')
print('')

for course in my_account.courses:
    print(course.course_name + ' by ' + course.teacher_name)
    if course.has_assignments:
        print('Assignments:')
        for assignment in course.get_assignments():
            print(assignment.title + ' due on ' + assignment.due_date.strftime('%d %b %Y'))
    else:
        print('Your teacher has not enabled assignments.')
    if course.has_assignment_marks:
        print('Assignment marks:')
        for assignment_mark in course.get_assignment_marks():
            print(assignment_mark.title + ' which you scored ' + assignment_mark.percent + ' in.')
    else:
        print('Your teacher has not enabled assignment mark viewing.')
    print('')
