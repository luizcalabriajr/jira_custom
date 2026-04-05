import requests
from requests.auth import HTTPBasicAuth

email = "SEU_EMAIL_DO_JIRA"
token = "SEU_TOKEN_API"

url = "https://xipptech.atlassian.net/rest/api/3/issuetype"

response = requests.get(url, auth=HTTPBasicAuth(email, token))

for t in response.json():
    print(f"{t['id']} - {t['name']}")