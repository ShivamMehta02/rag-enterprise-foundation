import requests

ACCESS_TOKEN = "1000.da0f74ffb01973aa0060f0b4cafe148f.1c79f1169af2fccebc6f46d7a4555775"
ORG_ID = "60065893464"

url = "https://www.zohoapis.in/inventory/v1/items"

headers = {
    "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}",
    "X-com-zoho-inventory-organizationid": ORG_ID
}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)
print(response.json())