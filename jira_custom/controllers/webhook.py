from odoo import http
from odoo.http import request
import json

class JiraWebhookController(http.Controller):

    @http.route('/jira/webhook', auth='public', methods=['POST'], csrf=False)
    def jira_webhook(self, **kwargs):
        try:
            payload = json.loads(request.httprequest.data)
        except Exception:
            return "Invalid JSON"

        issue = payload.get("issue", {})
        issue_key = issue.get("key")
        fields = issue.get("fields", {})
        status = fields.get("status", {}).get("name")

        if not issue_key:
            return "No issue key"

        jira_issue = request.env['jira.issue'].sudo().search([('name', '=', issue_key)], limit=1)
        if jira_issue:
            jira_issue.write({
                'status': status or jira_issue.status,
            })

        return "OK"
