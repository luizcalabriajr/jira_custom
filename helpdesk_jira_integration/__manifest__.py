{
    "name": "Helpdesk ↔ Jira Integration",
    "version": "18.0.1.0.0",
    "depends": ["helpdesk_mgmt", "jira_base"],
    'author': 'Luiz Calabria',
    "data": [
        "security/ir.model.access.csv",
        "views/jira_issue_views.xml",
        "views/helpdesk_ticket_views.xml",
    ],
    'installable': True,
    'application': True,
}
