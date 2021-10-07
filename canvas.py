import requests
import json
from requests.auth import HTTPBasicAuth

class Class:

    def __init__(self, id = None, name = None, term_id = None, assignments = None):
        self.id = id
        self.name = name
        self.assignments = []
        self.term_id = term_id

course_id = 0

# Class implementation of canvas API
class CanvasApi:
    def __init__(self, ApiToken, schoolPrefix = ''):
        self.ApiToken = ApiToken
        self.schoolPrefix = schoolPrefix
        self.header = {
            'Authorization': 'Bearer ' + self.ApiToken
        }
        self.courses = {}

    def get_course_objects(self):
        params = {'per_page': 50,'include': ['concluded']}
        readUrl = f'https://{self.schoolPrefix}.instructure.com/api/v1/courses'
        classes = []
        courses = requests.request('GET', readUrl, headers = self.header, params = params).json()

        for i in courses:
            if i.get('name') != None and i.get('enrollment_term_id') == 10738:
                name = i.get('name')

                if name != None:
                    name = name.replace(' ', '')

                cleanName = ""
                num = 0

                while name[num].isalpha() or name[num] == '/' or name[num] == '-':
                    cleanName += name[num]

                    if name[num] == name[-1]:
                        break

                    num += 1


                while name[num].isdigit() and num < 6:
                    cleanName += name[num]

                    if name[num] == name[-1]:
                        break

                    num += 1

                classObj = Class(i.get('id'), cleanName, i.get('enrollment_term_id'), i.get('assignments'))
                classes.append(classObj)

        return classes

    # Initialize self.courses dictionary with the key being

    def set_courses_and_id(self):
        for courseObject in self.get_course_objects():
            if courseObject != None:
                self.courses[courseObject.name] = courseObject.id

    # Return a courses id number given the courses name

    def get_course_id(self, courseName):
        return self.courses[courseName]


    # Returns a list of all assignment objects for a given course

    def get_assignment_objects(self, courseName, timeframe = None):
        readUrl = f'https://{self.schoolPrefix}.instructure.com/api/v1/courses/{self.courses[courseName]}/assignments/'

        params = {'per_page': 150, 'bucket': timeframe}

        assignments = requests.request('GET', readUrl, headers = self.header, params = params).json()
        assignmentList = []

        for assignment in assignments:
            if assignment['due_at'] == None:
                assignment['due_at'] = '2021-01-01T00:00:00Z'

            assignmentList.append(assignment)
            # print(assignment['due_at'])


        return assignmentList


    # Prints version of all currently enrolled classes

    def list_classes_names(self):
        for course in self.get_course_objects():
            print(course.name)
