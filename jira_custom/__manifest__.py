{
    'name': 'Jira Custom Integration',
    'version': '18.0.1.0.0',
    'summary': 'Integração direta com Jira via API e Webhooks',
    'author': 'Luiz + Copilot',
    'depends': ['base', 'mail'],
    'data': [
        'views/jira_issue_views.xml',
    ],
    'installable': True,
    'application': True,
}
