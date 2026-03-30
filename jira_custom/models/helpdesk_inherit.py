from odoo import models, fields, api
import requests
import json

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    jira_issue_id = fields.Many2one('jira.issue', string="Jira Issue")
    jira_key = fields.Char(related="jira_issue_id.name", string="Jira Key", readonly=True)
    jira_url = fields.Char(string="Jira URL", compute="_compute_jira_url")

    def _compute_jira_url(self):
        for rec in self:
            if rec.jira_key:
                rec.jira_url = f"https://SUA_ORGANIZACAO.atlassian.net/browse/{rec.jira_key}"
            else:
                rec.jira_url = False

    def action_create_jira_from_ticket(self):
        for ticket in self:
            issue = self.env['jira.issue'].create({
                'summary': ticket.name,
                'description': ticket.description or '',
                'project_key': 'TEST',  # você pode tornar isso configurável depois
            })
            issue.action_create_in_jira()
            ticket.jira_issue_id = issue.id
