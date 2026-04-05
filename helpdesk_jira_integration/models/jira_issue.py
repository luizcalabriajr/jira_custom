from odoo import models, fields # type: ignore
import json

class JiraIssue(models.Model):
    _name = "jira.issue"
    _description = "Jira Issue"

    jira_id = fields.Char(string="Chave Jira")
    summary = fields.Char()
    description = fields.Text()
    project_key = fields.Char(default=lambda self: self.env["ir.config_parameter"].sudo().get_param("jira.project_key"))
    status = fields.Char()
    synced = fields.Boolean(default=False)

    def action_create_in_jira(self):
        params = self.env["ir.config_parameter"].sudo()
        api = self.env["jira.api"]

        labels = params.get_param("jira.default_labels") or ""
        labels = [l.strip() for l in labels.split(",") if l.strip()]

        payload = {
            "fields": {
                "summary": self.summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {"type": "paragraph", "content": [{"type": "text", "text": self.description or ""}]}
                    ],
                },
                "project": {"key": params.get_param("jira.project_key")},
                "issuetype": {"id": params.get_param("jira.issue_type_id")},
                "reporter": {"id": params.get_param("jira.account_id")},
                "labels": labels,
            }
        }

        response = api.jira_post("/rest/api/3/issue", payload)

        if response.status_code == 201:
            data = response.json()
            self.jira_id = data["key"]
            self.synced = True
            self.status = "Criado com sucesso"
        else:
            self.status = f"Erro: {response.text}"
