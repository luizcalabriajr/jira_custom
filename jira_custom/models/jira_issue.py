import requests
import json
from odoo import models, fields, api # type: ignore

class JiraIssue(models.Model):
    _name = 'jira.issue'
    _description = 'Jira Issue'

    name = fields.Char(string="Jira Key")
    summary = fields.Char(string="Summary")
    description = fields.Text(string="Description")
    project_key = fields.Char(string="Project Key", default="TITESTE")  # <-- SEU PROJETO AQUI

    def action_create_in_jira(self):
        url = "https://xipptech.atlassian.net/rest/api/3/issue"
        auth_email = "SEU_EMAIL_DO_JIRA"
        auth_token = "SEU_TOKEN_API"

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "fields": {
                "summary": self.summary,
                "description": self.description or "",
                "project": {
                    "key": self.project_key  # <-- O Jira exige isso
                },
                "issuetype": {
                    "name": "Task"  # ou Bug, Story, etc.
                }
            }
        }

        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            auth=(auth_email, auth_token)
        )

        if response.status_code not in (200, 201):
            raise ValueError(
                f"Erro ao criar issue no Jira: {response.status_code} - {response.text}"
            )

        data = response.json()
        self.name = data.get("key")
