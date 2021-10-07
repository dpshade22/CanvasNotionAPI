import json, requests
import random
from canvas import CanvasApi
from notion import NotionApi


def createDatabase(canvasApi, NotionApi):
    canvasApi.set_courses_and_id()
    for course in canvasApi.get_course_objects():
        for assignment in canvasApi.get_assignment_objects(course.name, 'future'):
            NotionApi.createNewPage(className = course.name, dueDate = assignment['due_at'], assignmentName = assignment['name'], status = "To Do")



# EmptyEmpty.createNewPage(className = "MA322", assignmentName = "Assignment NAme", status = "To Do")
