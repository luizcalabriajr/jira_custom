import requests
import json
from requests.auth import HTTPBasicAuth

# 🔧 CONFIGURAÇÕES
email = "SEU_EMAIL_DO_JIRA"
token = "SEU_TOKEN_API"

project_key = "TITESTE"
issue_type = "Tarefa"  # coloque exatamente o nome do tipo de issue

url = (
    f"https://xipptech.atlassian.net/rest/api/3/issue/createmeta"
    f"?projectKeys={project_key}"
    f"&issuetypeNames={issue_type}"
    f"&expand=projects.issuetypes.fields"
)

response = requests.get(
    url,
    auth=HTTPBasicAuth(email, token),
    headers={"Accept": "application/json"}
)

if response.status_code != 200:
    print("Erro ao consultar o Jira:")
    print(response.text)
    exit()

data = response.json()

# Navega até os campos
fields = data["projects"][0]["issuetypes"][0]["fields"]

print("\n=== CAMPOS OBRIGATÓRIOS ===\n")
for field_id, field_info in fields.items():
    if field_info.get("required", False):
        print(f"- {field_id}  ({field_info.get('name')})")

print("\n=== TODOS OS CAMPOS ===\n")
for field_id, field_info in fields.items():
    print(f"{field_id}: {field_info.get('name')} (Obrigatório: {field_info.get('required')})")
