import requests, json, random

colors = ["default", "gray", "brown", "red", "orange", "yellow", "green", "blue", "purple", "pink"]


class NotionApi:
    def __init__(self, notionToken = None, database_id = None, version = None):
        self.database_id = database_id
        self.notionToken = notionToken
        self.notionHeaders ={
            'Authorization': 'Bearer ' + notionToken,
            'Content-Type': 'application/json',
            'Notion-Version': '2021-08-16'
        }

    def queryDatabase(self):
        readUrl = f'https://api.notion.com/v1/databases/{self.database_id}/query'

        res = requests.request('POST', readUrl, headers = self.notionHeaders)
        data = res.json()

        with open('./db.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii= False)


    def createNewPage(self, className, assignmentName, status, dueDate = '2021-01-01T00:00:00Z'):

        createUrl = 'https://api.notion.com/v1/pages'

        newPageData = {
            "parent": {
            "database_id": self.database_id
            },
            "properties": {
                "Assignment": {
                    "type": "title",
                    "title": [
                        {
                            "text": {
                                "content": assignmentName,
                            },
                            
                        }
                    ]
                },
                "Activity": {
                    "select": {
                        "name": className,
                    }
                },
                "Due Date": {
                    "date": {
                    "start": dueDate
                    }
                },
                "Status": {
                    "select": {
                            "name": status,
                            "color": 'orange'
                        }
                },
                
            },
        }
        
        data = json.dumps(newPageData)

        res = requests.request('POST', createUrl, headers = self.notionHeaders, data = data)
        
        print(res.text)

        return res

