import requests
import json
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from payload import create_project
from pydantic import BaseModel

load_dotenv()

class JiraSupport(BaseModel):
    email: str
    api_token: str
    domain: str

    def __repr__(self):
        return {f"Email: {self.email}, API Token: {self.api_token}, Domain: {self.domain}"}

    @property
    def auth(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(self.email, self.api_token)

    # Get the issues types
    def get_issues_types(self):
        url = f"https://{self.domain}.atlassian.net/rest/api/3/issue/createmeta"

        headers = {
        "Accept": "application/json"
        }

        response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=self.auth
        )

        return response.text

    # Create new project
    def create_new_project(self, project_key, project_name, project_description):
        url = f"https://{self.domain}.atlassian.net/rest/api/3/project"

        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

        payload = json.dumps(create_project(project_key, project_name))
        response = requests.request("POST", url, data=payload, headers=headers, auth=self.auth)

        return response


jira_support = JiraSupport(
    email=os.environ["JIRA_EMAIL"], 
    api_token=os.environ["JIRA_API_TOKEN"],
    domain=os.environ["JIRA_DOMAIN"]
)
