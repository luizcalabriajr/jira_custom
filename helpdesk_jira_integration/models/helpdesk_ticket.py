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

    def _update_status_from_jira(self, jira_status):
        try:
            status_map = {
                "To Do": "Novo",
                "In Progress": "Em Atendimento",
                "Done": "Resolvido",
                "Closed": "Fechado",
            }

            target_stage = status_map.get(jira_status)
            if not target_stage:
                self.jira_sync_status = f"Status Jira sem mapeamento: {jira_status}"
                return

            # Descobrir qual modelo de estágio existe
            StageModel = None
            for model in ["helpdesk.stage", "helpdesk.ticket.stage"]:
                if model in self.env:
                    StageModel = model
                    break

            if not StageModel:
                self.jira_sync_status = "Modelo de estágio não encontrado"
                return

            stage = self.env[StageModel].search([("name", "=", target_stage)], limit=1)
            if not stage:
                self.jira_sync_status = f"Estágio '{target_stage}' não encontrado"
                return

            # Descobrir qual campo de estágio existe
            for field in ["stage_id", "ticket_stage_id", "state_id", "kanban_state"]:
                if field in self._fields:
                    setattr(self, field, stage.id)
                    self.jira_sync_status = f"Atualizado do Jira: {jira_status}"
                    return

            self.jira_sync_status = "Nenhum campo de estágio encontrado"

        except Exception as e:
            self.jira_sync_status = f"Erro ao atualizar status: {str(e)}"
