from odoo import models, fields, api

class JiraSettings(models.Model):
    _name = "jira.settings"
    _description = "Jira Settings"

    jira_base_url = fields.Char(string="Jira Base URL")
    jira_email = fields.Char(string="Jira Email")
    jira_token = fields.Char(string="Jira Token", password=True)
    jira_account_id = fields.Char(string="Reporter Account ID")
    jira_project_key = fields.Char(string="Project Key")
    jira_issue_type_id = fields.Char(string="Issue Type ID")
    jira_default_labels = fields.Char(string="Default Labels (comma separated)")

    def write(self, vals):
        res = super().write(vals)
        params = self.env["ir.config_parameter"].sudo()

        for rec in self:
            params.set_param("jira.base_url", rec.jira_base_url)
            params.set_param("jira.email", rec.jira_email)
            params.set_param("jira.token", rec.jira_token)
            params.set_param("jira.account_id", rec.jira_account_id)
            params.set_param("jira.project_key", rec.jira_project_key)
            params.set_param("jira.issue_type_id", rec.jira_issue_type_id)
            params.set_param("jira.default_labels", rec.jira_default_labels)

        return res

    @api.model
    def load_settings(self):
        params = self.env["ir.config_parameter"].sudo()
        return {
            "jira_base_url": params.get_param("jira.base_url"),
            "jira_email": params.get_param("jira.email"),
            "jira_token": params.get_param("jira.token"),
            "jira_account_id": params.get_param("jira.account_id"),
            "jira_project_key": params.get_param("jira.project_key"),
            "jira_issue_type_id": params.get_param("jira.issue_type_id"),
            "jira_default_labels": params.get_param("jira.default_labels"),
        }
