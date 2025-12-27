import requests
import json
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from payload import create_issue, create_project

# Global Storage
db_projects = []

# Load variables from .env file
load_dotenv()

# Authentication
auth = HTTPBasicAuth(os.environ["JIRA_EMAIL"], os.environ["JIRA_API_TOKEN"])

# Server url
server = os.environ["JIRA_SERVER"]

# Function to print the code of HTTP to the console
def print_status(response) -> None:
    print(f"{response.request.method} Status: {response.status_code} {response.request.url}")

# Get the issues types
print("Getting issue types")
url = server + "/rest/api/3/issue/createmeta"

headers = {
  "Accept": "application/json"
}

response = requests.request(
   "GET",
   url,
   headers=headers,
   auth=auth
)

print_status(response)
# print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


# Create new issue
print("Creating issue")
url = server + "/rest/api/2/issue"

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

payload = json.dumps(create_issue("SCRUM", "BUG", "Fix Bug", "Bug on the frontend in section cards"))
response = requests.request("POST", url, data=payload, headers=headers, auth=auth)
print_status(response)
#print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


# Get the projects list
print("Searching all projects")
headers = {
  "Accept": "application/json"
}

url = server + "/rest/api/3/project/search"
response = requests.request("GET", url, headers=headers, auth=auth)
print_status(response)
data = response.json()
#print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


if response.status_code == 200:
    for project in data["values"]:
      db_projects.append(project["key"]) 
else:
   print("Failed to extract data")


# Create new project
print("Creating new project")
url = server + "/rest/api/3/project"

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

payload = json.dumps(create_project("SCRUMTE", "TEST PROJECT Test22", "Test Project Description22", "PROJECT_LEAD"))
response = requests.request("POST", url, data=payload, headers=headers, auth=auth)
print_status(response)
print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
if response.status_code == 201:
   db_projects.append(response.text["key"])
print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

# Get Users Info
print("Get users info")
url = server + "/rest/api/3/users/search"
headers = {
  "Accept": "application/json"
}

response = requests.request("GET", url, headers=headers, auth=auth)
print_status(response)
#print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

print(db_projects)