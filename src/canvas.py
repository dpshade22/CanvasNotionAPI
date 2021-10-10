import requests, json
from datetime import date
from dateutil.relativedelta import relativedelta
from requests.auth import HTTPBasicAuth


class Class:
    def __init__(self, id=None, name=None, term_id=None, assignments=None):
        self.id = id
        self.name = name
        self.assignments = []
        self.term_id = term_id


course_id = 0

# Class implementation of canvas API
class CanvasApi:
    def __init__(self, canvasKey, schoolPrefix=""):
        self.canvasKey = canvasKey
        self.schoolPrefix = schoolPrefix
        self.header = {"Authorization": "Bearer " + self.canvasKey}
        self.courses = {}

    def get_courses_within_six_months(self):
        params = {
            "per_page": 200,
            "include": ["concluded"],
            "enrollment_state": ["active"],
        }
        readUrl = f"https://{self.schoolPrefix}.instructure.com/api/v1/courses"
        classes = []
        courses = requests.request(
            "GET", readUrl, headers=self.header, params=params
        ).json()

        for course in courses:
            datedate = ""
            ndx = 0

            if course.get("start_at") != None:
                while course.get("start_at")[ndx] != "T":
                    datedate += course.get("start_at")[ndx]
                    ndx += 1

                j = date.fromisoformat(datedate)
                six_months_ago = date.today() - relativedelta(months=6)

            if j < six_months_ago:
                continue

            if course.get("name") != None:
                name = course.get("name")
                name = cleanCourseName(name)

                classObj = Class(
                    course.get("id"),
                    name,
                    course.get("enrollment_term_id"),
                    course.get("assignments"),
                )

                if j < six_months_ago:
                    continue
                else:
                    classes.append(classObj)
        return classes

    def get_all_courses(self):
        params = {
            "per_page": 200,
            "include": ["concluded"],
            "enrollment_state": ["active"],
        }
        readUrl = f"https://{self.schoolPrefix}.instructure.com/api/v1/courses"
        classes = []
        courses = requests.request(
            "GET", readUrl, headers=self.header, params=params
        ).json()

        for i in courses:
            if i.get("name") != None:
                name = i.get("name")
                name = cleanCourseName(name)

                classObj = Class(
                    i.get("id"),
                    name,
                    i.get("enrollment_term_id"),
                    i.get("assignments"),
                )
                classes.append(classObj)
        return classes

    # Initialize self.courses dictionary with the key being
    def set_courses_and_id(self):
        for courseObject in self.get_all_courses():
            if courseObject != None:
                self.courses[courseObject.name] = courseObject.id

    # Return a courses id number given the courses name
    def get_course_id(self, courseName):
        return self.courses[courseName]

    # Returns a list of all assignment objects for a given course
    def get_assignment_objects(self, courseName, timeframe=None):
        readUrl = f"https://{self.schoolPrefix}.instructure.com/api/v1/courses/{self.courses[courseName]}/assignments/"
        params = {"per_page": 500, "bucket": timeframe}

        assignments = requests.request(
            "GET", readUrl, headers=self.header, params=params
        ).json()
        assignmentList = []

        for assignment in assignments:
            i = 0
            newDueDate = ""
            if assignment.get("due_at") == None:
                assignment["due_at"] = "2021-01-01"
            else:
                while assignment["due_at"][i] != "T":
                    newDueDate += assignment["due_at"][i]
                    i += 1
                assignment["due_at"] = newDueDate

            assignment["url"] = assignment["html_url"]
            assignmentList.append(assignment)

        return assignmentList

    # Prints version of all currently enrolled classes
    def update_assignment_objects(
        self, notionAssignmentsList, courseName, timeframe=None
    ):
        readUrl = f"https://{self.schoolPrefix}.instructure.com/api/v1/courses/{self.courses[courseName]}/assignments/"
        params = {"per_page": 500, "bucket": timeframe}

        assignments = requests.request(
            "GET", readUrl, headers=self.header, params=params
        ).json()
        assignmentList = []

        for assignment in assignments:
            i = 0
            newDueDate = ""
            if assignment.get("due_at") == None:
                assignment["due_at"] = None
            else:
                while assignment["due_at"][i] != "T":
                    newDueDate += assignment["due_at"][i]
                    i += 1
                assignment["due_at"] = newDueDate

            assignment["url"] = assignment["html_url"]

            if assignment["url"] not in notionAssignmentsList:
                assignmentList.append(assignment)

        return assignmentList

    def list_classes_names(self):
        for course in self.get_course_objects():
            print(course.name)


def cleanCourseName(name):
    cleanName = ""
    num = 0

    if name != None:
        name = name.replace(" ", "")

    while name[num].isalpha() or name[num] == "/" or name[num] == "-":
        cleanName += name[num]

        if name[num] == name[-1]:
            break

        num += 1

    while name[num].isdigit() and num < 6:
        cleanName += name[num]

        if name[num] == name[-1]:
            break

        num += 1
    return cleanName
