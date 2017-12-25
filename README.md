![St. Michaels University School SDS](https://i.imgur.com/5wEKs0H.png?1)
# SMUS SDS Parser
A python library that parses the St. Michaels University School School Data System student panel

#### Installation
To install, clone this repository somehere on your system and then `import smusdsparser` into your project.

#### Usage
The first step is creating a session. Currently, you cannot setup a session using your username and password ([view issue](https://github.com/rashidx/SMUS-SDS-Parser/issues/1)).
```python
# The session_id can be obtained by logging into SMUS SDS and using a chrome extension like EditThisCookie to find
# the PHPSESSID cookie value.
session_id = 'd59gobaahijptjm6rirp7dika5'

# The first step is creating our session
my_session = smussdsparser.Session(session_id)
```
Using the session that we just created, you can request a variety of information. You can create a student object that holds all your data.
```python
# We create a student object by passing our session to the Student class
my_account = smussdsparser.Student(my_session)

# Student objects have many attributes including name and courses
print('Welcome ' + my_account.name + '.')
print('You are currently enrolled in ' + str(len(my_account.courses)) + 'courses.')
```
You can also loop over your courses and request assignment information.
```python
for course in my_account.courses:
    print(course.course_name + ' by ' + course.teacher_name)
    if course.has_assignments:
        print('Assignments:')
        for assignment in course.get_assignments():
            print(assignment.title + ' due on ' + assignment.due_date.strftime('%d %b %Y'))
    else:
        print('Your teacher has not enabled assignments.')
```
Additionally, you can view your grades (as long as the teacher has enabled the feature).
```python
for course in my_account.courses:
    print(course.course_name + ' by ' + course.teacher_name)
    if course.has_assignment_marks:
        print('Assignment marks:')
        for assignment_mark in course.get_assignment_marks():
            print(assignment_mark.title + ' which you scored ' + assignment_mark.percent + ' in.')
    else:
        print('Your teacher has not enabled assignment mark viewing.')
```

#### What's the motivaton behind this?
If you are a St. Michaels University School student, you know how old the School Data System (or SDS for short) look and feels. For that reason, I have created this library to aid in the creation of an API that would encourage current SMUS students to develop their own front-end.
