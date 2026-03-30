{
    'name': 'Jira Custom Integration',
    'version': '18.0.1.0.0',
    'summary': 'Integração direta com Jira via API e Webhooks',
    'author': 'Luiz Calabria',
    'depends': ['base', 'mail'],
    'data': [
    'security/jira_groups.xml',
    'security/ir.model.access.csv',
    'views/jira_issue_views.xml',
    'views/helpdesk_views.xml',
    ],
    'installable': True,
    'application': True,
}
