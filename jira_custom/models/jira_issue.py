from odoo import models, fields, api
import requests

class JiraIssue(models.Model):
    _name = 'jira.issue'
    _description = 'Jira Issue'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Issue Key", tracking=True)
    summary = fields.Char("Summary", required=True, tracking=True)
    description = fields.Text("Description")
    jira_id = fields.Char("Jira ID", readonly=True)
    status = fields.Char("Status", tracking=True)
    project_key = fields.Char("Project Key", required=True)
    synced = fields.Boolean("Synced with Jira", default=False)

    def _get_jira_headers(self):
        # ⚠️ Ajuste aqui: use sua API key e email do Jira
        api_token = "SUA_API_KEY"
        email = "SEU_EMAIL_NO_JIRA"
        from base64 import b64encode
        auth = b64encode(f"{email}:{api_token}".encode()).decode()
        return {
            "Authorization": f"Basic {auth}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _get_jira_base_url(self):
        # ⚠️ Ajuste aqui: seu domínio Jira Cloud
        return "https://SUA_ORGANIZACAO.atlassian.net"

    def action_create_in_jira(self):
        for rec in self:
            if rec.jira_id:
                continue

            url = f"{rec._get_jira_base_url()}/rest/api/3/issue"
            headers = rec._get_jira_headers()
            payload = {
                "fields": {
                    "project": {"key": rec.project_key},
                    "summary": rec.summary,
                    "description": rec.description or "",
                    "issuetype": {"name": "Task"},
                }
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 201:
                data = response.json()
                rec.jira_id = data.get("id")
                rec.name = data.get("key")
                rec.synced = True
            else:
                raise ValueError(f"Erro ao criar issue no Jira: {response.status_code} - {response.text}")

    def action_open_in_jira(self):
        for rec in self:
            if not rec.name:
                continue
            base = rec._get_jira_base_url()
            return {
                'type': 'ir.actions.act_url',
                'url': f"{base}/browse/{rec.name}",
                'target': 'new',
            }
