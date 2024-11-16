import requests
import json

url = "http://ramzinex.com/exchange/api/v1.0/exchange/auth/api_key/getToken"

payload = json.dumps({
  "secret": "50b9618023a67229f41e6ffbfa28c51a",
  "api_key": "ApiKeysQXQ2Av:9dbc891d1845faadfc239ab1cc54ad1b27565390fbd141125fafe712e039e762"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
