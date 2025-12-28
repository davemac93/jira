import os
import json
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from jira import JIRA, JIRAError
from pprint import pprint
from support import JiraSupport


# Storage
db_projects = []
db_issue = []

# Load variables from .env file
load_dotenv()

# Authentication
jira = JIRA(
    server=os.environ["JIRA_SERVER"],
    basic_auth=(os.environ["JIRA_EMAIL"], os.environ["JIRA_API_TOKEN"])
)

# Own Class for the RESTAPI 

jira_support = JiraSupport(
    email=os.environ["JIRA_EMAIL"], 
    api_token=os.environ["JIRA_API_TOKEN"],
    domain=os.environ["JIRA_DOMAIN"]
)



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
            'issues': []
        }
        db.append(details)

    return db

# Create Project
def create_new_project(project_key, project_name):
        projects = get_projects()

        if any(p["key"] == project_key for p in projects):
            print(f"Project {project_key} already exists")
            return None
        else:
            project = jira_support.create_project(project_key.upper(), project_name)
            if project.status_code == 201:
                print(f"Project key {project_key} created")
            else:
                print(f"Error the request to create project: {project} {project.text}")
                return None
        return project



# Get all issue
def get_issues(db_projects):
    count = 0
    for project in db_projects:
        project_key = project['key']
        issues = jira.search_issues(f"project={project_key}")
        for issue in issues:
            details = {
                'key': issue.key,
                'id': issue.id
            }
            db_projects[count]['issues'].append(details)
        count += 1
    return db_projects



# Create issue
def create_issue(project_key, summary, description, issue_type="Task"):
    issue_dict = {
        'project': {'key': project_key},
        'summary': summary,
        'description': description,
        'issuetype': {'name': issue_type},

    }
    new_issue = jira.create_issue(fields=issue_dict)
    return new_issue

# Update issue
def update_issue(issue_key, summary, description):
    issue = jira.issue(issue_key)
    issue.update(summary=summary, description=description)

# Assign all unasigned issues
def assign_issue_to_user(issue_key, user_id):
    issue = jira.issue(issue_key)
    if issue.fields.assignee == None:
        print(f"Update user for: {user_id}")
        issue.update(assignee={'accountId': f'{user_id}' })
    else: 
        print("Update user failed: Because user alreacy assign to the issue")

# Assign issues to a sprint on a project
def update_issue_sprint(issue_key, sprint_id):
    issue = jira.issue(issue_key)
    issue.update(customfield_10020=sprint_id)

# Get all the spring
def get_springs_id():
    db = []
    boards = jira.boards()
    for board in boards:
        sprints = jira.sprints(board.id)
        for sprint in sprints:
            details = {
                'name': sprint.name,
                'id': sprint.id
            }
            db.append(details)
    return db


db_projects = get_projects()
db_projects = get_issues(db_projects)

#pprint(db_projects, indent=1)

# Test Connection
try:
    my_user = jira.myself()
    print(f"Your User ID: {my_user['accountId']}")
except Exception as e:
    print("An error occurred:", e)

#Create Project 
try:
    respose = create_new_project("TEST25", "Test25")
except Exception as e:
    print(f"Error on creating a project: {e}")

# Create Issue
try:
    issue = create_issue("SCRUM", "Test for the SCRUM", "Test for the SCRUM", issue_type="Task")
    print(f"Ticket created: {issue}")
except Exception as e:
    print(f"Error on creating the issue: {e}")
 
# Update Issue
try:
    update_issue(issue, "New summary", "New Description") 
except Exception as e:
    print(f"Error on updating issue: {e}")

# Assign someone to issue 
try:
    assign_issue_to_user(issue, my_user['accountId'])
except Exception as e:
    print(f"Error on the assigment: {e}")


