from odoo import models, fields, api

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    jira_issue_id = fields.Many2one("jira.issue")
    jira_key = fields.Char(related="jira_issue_id.jira_id", readonly=True)
    jira_url = fields.Char(compute="_compute_jira_url")
    jira_sync_status = fields.Char()

    def _compute_jira_url(self):
        for rec in self:
            rec.jira_url = (
                f"https://xipptech.atlassian.net/browse/{rec.jira_key}"
                if rec.jira_key else False
            )

    def action_create_jira_from_ticket(self):
        issue = self.env["jira.issue"].create({
            "summary": self.name,
            "description": self.description or "",
        })
        issue.action_create_in_jira()
        self.jira_issue_id = issue.id
        self.jira_sync_status = issue.status

    @api.model
    def create(self, vals):
        ticket = super().create(vals)

        issue = ticket.env["jira.issue"].create({
            "summary": ticket.name,
            "description": ticket.description or "",
        })

        issue.action_create_in_jira()

        ticket.jira_issue_id = issue.id
        ticket.jira_sync_status = issue.status

        return ticket