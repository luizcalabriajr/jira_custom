import requests
import base64

email = "SEU_EMAIL_DO_JIRA"
token = "SEU_TOKEN_API"

auth = base64.b64encode(f"{email}:{token}".encode()).decode()

url = "https://xipptech.atlassian.net/rest/api/3/issuetype"

headers = {
    "Authorization": f"Basic {auth}",
    "Accept": "application/json"
}

import requests
response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)
