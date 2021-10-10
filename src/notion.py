import requests, json


class NotionApi:
    def __init__(
        self,
        notionToken=None,
        database_id=None,
        schoolAb=None,
        version="2021-08-16",
    ):
        self.database_id = database_id
        self.notionToken = notionToken
        self.schoolAb = schoolAb
        self.notionHeaders = {
            "Authorization": "Bearer " + notionToken,
            "Content-Type": "application/json",
            "Notion-Version": "2021-08-16",
        }

    def queryDatabase(self):
        readUrl = f"https://api.notion.com/v1/databases/{self.database_id}/query"

        res = requests.request("POST", readUrl, headers=self.notionHeaders)
        data = res.json()

        with open("./db.json", "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False)

        return data

    def test_if_database_id_exists(self):
        res = requests.request(
            "GET",
            f"https://api.notion.com/v1/databases/{self.database_id}/",
            headers=self.notionHeaders,
        )

        return json.loads(res.text)["object"] != "error"

    # Creates a new database in page_id page built for Canvas assignments and returns it's database_id
    def createNewDatabase(self, page_id):
        newPageData = {
            "parent": {
                "type": "page_id",
                "page_id": page_id,
            },
            "icon": {"type": "emoji", "emoji": "🔖"},
            "cover": {
                "type": "external",
                "external": {"url": "https://website.domain/images/image.png"},
            },
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": "Canvas Assignments",
                        "link": None,
                    },
                }
            ],
            "properties": {
                "Status": {
                    "select": {
                        "options": [
                            {"name": "To Do", "color": "pink"},
                            {"name": "In Progress", "color": "red"},
                            {"name": "Completed", "color": "green"},
                        ]
                    }
                },
                "Assignment": {"title": {}},
                "Class": {
                    "type": "select",
                    "select": {"options": []},
                },
                "Due Date": {"date": {}},
                "URL": {"url": {}},
            },
        }

        data = json.dumps(newPageData)

        res = requests.request(
            "POST",
            "https://api.notion.com/v1/databases",
            headers=self.notionHeaders,
            data=data,
        )

        newDbId = json.loads(res.text).get("id")

        return newDbId

    def createNewDatabaseItem(
        self,
        id,
        className,
        assignmentName,
        status,
        url=None,
        dueDate=None,
    ):
        if dueDate["start"] == None:
            dueDate = None

        createUrl = "https://api.notion.com/v1/pages"

        newPageData = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Status": {"select": {"name": status, "color": "pink"}},
                "Assignment": {
                    "type": "title",
                    "title": [
                        {
                            "text": {
                                "content": assignmentName,
                            },
                        }
                    ],
                },
                "Class": {
                    "select": {
                        "name": className,
                    }
                },
                "Due Date": {"date": dueDate},
                "URL": {
                    "url": url,
                },
            },
        }

        data = json.dumps(newPageData)

        res = requests.request("POST", createUrl, headers=self.notionHeaders, data=data)

        print(res.text)

        return res

    def parseDatabaseForAssignments(self):
        urls = []

        if self.queryDatabase().get("results") != None:
            for item in self.queryDatabase().get("results"):
                urls.append(item["properties"]["URL"]["url"])

        return urls
