import requests
from requests.auth import HTTPBasicAuth

email = "luizcalabria@xipptech.com.br"
token = ""

url = "https://xipptech.atlassian.net/rest/api/3/myself"

response = requests.get(url, auth=HTTPBasicAuth(email, token))

print(response.json())