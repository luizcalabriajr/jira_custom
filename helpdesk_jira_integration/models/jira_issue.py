from odoo import models, fields
import json

class JiraIssue(models.Model):
    _name = "jira.issue"
    _description = "Jira Issue"

    jira_id = fields.Char(string="Chave Jira")
    summary = fields.Char()
    description = fields.Text()
    project_key = fields.Char(default="TITESTE")
    status = fields.Char()
    synced = fields.Boolean(default=False)

    def action_create_in_jira(self):
        api = self.env["jira.api"]
        payload = {
            "fields": {
                "summary": self.summary,
                "description": {"type": "doc", "version": 1, "content": []},
                "project": {"key": self.project_key},
                "issuetype": {"id": "10114"},
                "reporter": {"id": "SEU_ACCOUNT_ID"},
                "labels": ["labels", "PRODUÇÃO"],
            }
        }
        response = api.jira_post("/rest/api/3/issue", payload)
        if response.status_code == 201:
            data = response.json()
            self.jira_id = data["key"]
            self.synced = True
            self.status = "Criado com sucesso"
