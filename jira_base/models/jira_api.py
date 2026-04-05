import requests
from requests.auth import HTTPBasicAuth
from odoo import models

class JiraAPI(models.AbstractModel):
    _name = "jira.api"
    _description = "Jira API Base"

    def _auth(self):
        return HTTPBasicAuth(
            self.env["ir.config_parameter"].sudo().get_param("jira.email"),
            self.env["ir.config_parameter"].sudo().get_param("jira.token"),
        )

    def _base_url(self):
        return self.env["ir.config_parameter"].sudo().get_param("jira.base_url")

    def jira_get(self, endpoint):
        url = f"{self._base_url()}{endpoint}"
        return requests.get(url, auth=self._auth(), headers={"Accept": "application/json"})

    def jira_post(self, endpoint, payload=None, files=None, headers=None):
        url = f"{self._base_url()}{endpoint}"
        default_headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)
        return requests.post(
            url,
            json=payload,
            files=files,
            auth=self._auth(),
            headers=default_headers,
        )
