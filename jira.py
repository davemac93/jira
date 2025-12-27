from jira import JIRA
from dotenv import load_dotenv
import os
from fastapi import FastAPI

## FastAPI Connection

app = FastAPI()

## JIRA REST API

#Storage
db_projects = []

# Load variables from .env file
load_dotenv()

# Authentication
jira = JIRA(
    server=os.environ["JIRA_SERVER"],
    basic_auth=(os.environ["JIRA_EMAIL"], os.environ["JIRA_API_TOKEN"])
)

# Test Connection
try:
    my_user = jira.myself()
    print(my_user['accountId'])
except Exception as e:
    print("An error occurred:", e)


all_users = jira.user()

print(all_users)

# Get all the Projects
def get_projects():
    projects = jira.projects()
    db = []

    for project in projects:
        details = {
            'key': project.key,
            'name': project.name,
            'id': project.id,
            'project_type': project.projectTypeKey,
        }
        db.append(details)

    return db

db_projects = get_projects()
print(db_projects)