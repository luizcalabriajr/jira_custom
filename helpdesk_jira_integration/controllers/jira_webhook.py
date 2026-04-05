from odoo import http
from odoo.http import request

class JiraWebhookController(http.Controller):

    @http.route('/jira/webhook', type='json', auth='public', methods=['POST'], csrf=False)
    def jira_webhook(self, **payload):
        issue = payload.get("issue", {})
        key = issue.get("key")
        fields = issue.get("fields", {})
        status = fields.get("status", {}).get("name")

        if not key or not status:
            return {"error": "Invalid payload"}

        # Buscar ticket vinculado
        jira_issue = request.env["jira.issue"].sudo().search([("jira_id", "=", key)], limit=1)
        if not jira_issue:
            return {"error": "Issue not found"}

        ticket = request.env["helpdesk.ticket"].sudo().search([("jira_issue_id", "=", jira_issue.id)], limit=1)
        if not ticket:
            return {"error": "Ticket not found"}

        # Atualizar status do ticket
        ticket._update_status_from_jira(status)

        return {"success": True}
