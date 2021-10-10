import json, requests
from canvas import CanvasApi
from notion import NotionApi


class User:
    def __init__(
        self,
        canvasKey,
        notionToken,
        notionPageId,
        schoolAb,
        database_id=None,
    ):
        self.notionToken = notionToken
        self.database_id = database_id
        self.canvasProfile = CanvasApi(canvasKey, schoolAb)
        self.page_ids = {"Default": notionPageId}
        self.generated_db_id = None
        self.schoolAb = schoolAb
        self.notionProfile = NotionApi(
            notionToken,
            database_id=database_id,
            schoolAb=schoolAb,
        )

    def getCoursesLastSixMonths(self):
        return self.canvasProfile.get_courses_within_six_months()

    def getAllCourses(self):
        return self.canvasProfile.get_all_courses()

    # Enters assignments into given database given (by id), or creates a new database, and fills the page with assignments not already found in the database
    def enterAssignmentsToNotionDb(self, courseList):
        if not self.notionProfile.test_if_database_id_exists():
            self.notionProfile = NotionApi(
                self.notionToken,
                database_id=self.createDatabase(),
                schoolAb=self.schoolAb,
            )
            self.addNewDatabaseItems(courseList)
        else:
            self.addNewDatabaseItems(courseList)

    # Creates a new Canvas Assignments database in the notionPageId page
    def createDatabase(self, page_id_name="Default"):
        return self.notionProfile.createNewDatabase(self.page_ids[page_id_name])

    # This function adds NEW assignments to the database based on whether the assignments URL can be found in the notion database
    def addNewDatabaseItems(self, courseList):
        self.canvasProfile.set_courses_and_id()
        for course in courseList:
            for assignment in self.canvasProfile.update_assignment_objects(
                self.notionProfile.parseDatabaseForAssignments(),
                course.name,
                "future",
            ):
                self.notionProfile.createNewDatabaseItem(
                    id=assignment["id"],
                    className=course.name,
                    dueDate={"start": assignment["due_at"]},
                    url=assignment["url"],
                    assignmentName=assignment["name"],
                    status="To Do",
                )

    # This function adds all found assignments to the notion database
    def rawFillDatabase(self, courseList):
        self.canvasProfile.set_courses_and_id()
        for course in courseList:
            for assignment in self.canvasProfile.get_assignment_objects(
                course.name, "future"
            ):
                self.notionProfile.createNewDatabaseItem(
                    id=assignment["id"],
                    className=course.name,
                    dueDate=assignment["due_at"],
                    url=assignment["url"],
                    assignmentName=assignment["name"],
                    status="To Do",
                )
