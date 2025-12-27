def create_issue(project_key, issue_type, summary, description_text):

    return {
    "fields": {
       "project":
       {
          "key": project_key
       },
       "summary": summary,
       "description": description_text,
       "issuetype": {
          "name": issue_type
       }
   }
}

def create_project(project_key, project_name, project_description, assignee="UNASSIGNED"):
    return {
  "key": project_key,
  "leadAccountId": "712020:66cfb0a7-db17-46c9-91c5-c938844ceadc",
  "name": project_name,
  "projectTypeKey": "software"
}