# Jira Automate 🚀

**Jira API integration utilities (Python)** — simple scripts and helpers to interact with Jira via the REST API and via the `jira` Python library.

---

## 🔎 Overview

This repository contains small utilities to list and manage Jira projects and issues. It provides two approaches:

- `main.py` — high-level functions using the `jira` (python-jira) library for common operations (list projects, create issues, assign, sprints). 
- `restAPI.py` — examples of direct REST calls using `requests`.
- `support.py` — a lightweight helper (`JiraSupport`) that wraps some REST calls.
- `payload.py` — helper functions that generate JSON payloads for requests.

> Note: The project currently includes usage examples that run immediately when the script is executed. See **Notes & known issues** below.

---

## ✅ Features

- Connect to Jira using API Token authentication
- List projects and issues
- Create projects and issues (example payloads provided)
- Simple wrapper (`JiraSupport`) for REST calls

---

## 🛠️ Prerequisites

- Python 3.10+ installed
- A Jira account with API token (Atlassian Cloud)
- Project admin permission for creating projects (if you plan to use project creation)

Install dependencies:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🔐 Environment variables

Create a `.env` file in the repository root with these variables:

```ini
# .env example
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_api_token
JIRA_SERVER=https://your-domain.atlassian.net   # full URL used by some scripts
JIRA_DOMAIN=your-domain                         # domain string (used by JiraSupport, e.g. 'your-domain')
```

> Important: Do NOT commit your `.env` file or API tokens to source control. Add them to `.gitignore` if not already present.

---

## ▶️ How to run

- Run the high-level helper script (`main.py`):

```bash
python main.py
```

`main.py` demonstrates:
- creating `JIRA` client from `jira` library
- `get_projects()`, `get_issues()`, `create_issue()`, `update_issue()` and other functions

- Run the raw REST example (`restAPI.py`):

```bash
python restAPI.py
```

`restAPI.py` performs a sequence of REST calls using `requests` and prints responses. Be careful — it executes calls on import / execution.

---

## 📁 Files overview

- `main.py` — high-level Jira operations via `jira` (python-jira)
- `restAPI.py` — example requests-based REST calls (GET / POST examples)
- `support.py` — `JiraSupport` class (thin wrapper around `requests` for REST calls)
- `payload.py` — small helpers to build request payloads
- `requirements.txt` — pinned dependencies

---

## ⚠️ Notes & known issues (found while scanning the code)

- `payload.create_project()` signature and usage differ in places:
  - `payload.create_project` currently takes `(project_key, project_name)` and returns a payload with a hard-coded `leadAccountId`.
  - `restAPI.py` calls `create_project` with four arguments which will raise a `TypeError`.
  - Suggestion: Update `payload.create_project` to accept `leadAccountId` and optional `project_description`, or update callers.

- Several places assume responses are JSON objects but use `response.text` as if it were a dict (e.g., `response.text["key"]`) — this will fail. Use `response.json()` first and validate before indexing.

- Some scripts execute example calls at import time (no `if __name__ == '__main__':` guard). Wrap executable example code in that guard to avoid accidental execution when importing.

- `restAPI.py` contains some hard-coded values (e.g., explicit URL to `testmbank.atlassian.net`) — update to use `JIRA_DOMAIN`/`JIRA_SERVER` env vars.

- `payload.create_project` contains a hard-coded `leadAccountId`. Replace with configurable value or make optional.

---

## 💡 Suggestions & next steps

- Add small CLI or argument parsing to choose actions (list, create-issue, create-project) rather than always executing everything.
- Add unit tests for payloads and wrapper functions.
- Add error handling and response validation for all requests.
- Consider adding a minimal FastAPI wrapper (if you want an HTTP API) — currently the project includes FastAPI in `requirements.txt` but no `app` file is present.

---

## ➕ Contributing

PRs are welcome — please include tests and update the README with any new features.

---

## 📜 License

Add your license here.

---

If you want, I can also:
- open a PR with the README changes, or
- fix the issues I listed (e.g., update `payload.create_project` and `restAPI.py` to be consistent), or
- add a simple CLI and a `--dry-run` mode to `restAPI.py`.

Let me know which you'd prefer! ✅