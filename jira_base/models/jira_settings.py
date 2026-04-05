from odoo import models, fields, api

class JiraSettings(models.TransientModel):
    _inherit = "res.config.settings"

    jira_base_url = fields.Char(string="Jira Base URL")
    jira_email = fields.Char(string="Jira Email")
    jira_token = fields.Char(string="Jira Token")
    jira_account_id = fields.Char(string="Reporter Account ID")
    jira_project_key = fields.Char(string="Project Key")
    jira_issue_type_id = fields.Char(string="Issue Type ID")
    jira_default_labels = fields.Char(string="Default Labels (comma separated)")

    def set_values(self):
        super().set_values()
        params = self.env["ir.config_parameter"].sudo()

        params.set_param("jira.base_url", self.jira_base_url)
        params.set_param("jira.email", self.jira_email)
        params.set_param("jira.token", self.jira_token)
        params.set_param("jira.account_id", self.jira_account_id)
        params.set_param("jira.project_key", self.jira_project_key)
        params.set_param("jira.issue_type_id", self.jira_issue_type_id)
        params.set_param("jira.default_labels", self.jira_default_labels)

    @api.model
    def get_values(self):
        res = super().get_values()
        params = self.env["ir.config_parameter"].sudo()

        res.update(
            jira_base_url=params.get_param("jira.base_url"),
            jira_email=params.get_param("jira.email"),
            jira_token=params.get_param("jira.token"),
            jira_account_id=params.get_param("jira.account_id"),
            jira_project_key=params.get_param("jira.project_key"),
            jira_issue_type_id=params.get_param("jira.issue_type_id"),
            jira_default_labels=params.get_param("jira.default_labels"),
        )
        return res
