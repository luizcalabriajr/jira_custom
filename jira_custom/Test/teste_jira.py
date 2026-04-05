import requests
import json
import base64

email = "SEU_EMAIL_DO_JIRA"
token = "SEU_TOKEN_API"

auth_string = f"{email}:{token}"
auth_base64 = base64.b64encode(auth_string.encode()).decode()

url = "https://xipptech.atlassian.net/rest/api/3/issue"

headers = {
    "Authorization": f"Basic {auth_base64}",
    "Content-Type": "application/json"
}

payload = {
    "fields": {
        "summary": "Teste via Python",
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "Descrição criada via API"}
                    ]
                }
            ]
        },
        "project": {"key": "TITESTE"},
        "issuetype": {"id": "10114"},
        "labels": ["labels", "PRODUÇÃO"]
    }
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print(response.status_code)
print(response.text)
