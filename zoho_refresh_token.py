import requests

client_id = "1000.OSPF1WKWWBA82CLP5ED928JJOE9MFY"
client_secret = "bba4cdf8f3652ba81663772545c434c8bbedcab456"
refresh_token = "1000.da31a935d9f883e58ac1e31cfab83053.16dbbb2aef406a88dfb759637e346361"

url = "https://accounts.zoho.in/oauth/v2/token"

data = {
    "refresh_token": refresh_token,
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "refresh_token"
}

response = requests.post(url, data=data)

print("Status:", response.status_code)
print(response.json())