import requests

ACCESS_TOKEN = "1000.da0f74ffb01973aa0060f0b4cafe148f.1c79f1169af2fccebc6f46d7a4555775"
ORG_ID = "60065893464"

def fetch_zoho_documents():

    url = "https://www.zohoapis.in/inventory/v1/items"

    headers = {
        "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}",
        "X-com-zoho-inventory-organizationid": ORG_ID
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("API Error:", response.text)
        return []

    data = response.json()
    items = data.get("items", [])

    documents = []

    for item in items:
        name = item.get("name", "Unknown item")
        brand = item.get("brand", "Unknown brand")
        manufacturer = item.get("manufacturer", "Unknown manufacturer")
        price = item.get("rate", "Unknown price")
        sku = item.get("sku", "Unknown SKU")
        product_type = item.get("product_type", "Unknown type")

        text = (
            f"{name} is a product from brand {brand}, manufactured by {manufacturer}. "
            f"It costs {price} rupees and has SKU {sku}. "
            f"It belongs to the category {product_type}."
        )

        documents.append({
            "text": text,
            "metadata": {
                "sku": sku,
                "brand": brand,
                "price": price
            }
        })

    return documents


if __name__ == "__main__":
    docs = fetch_zoho_documents()

    print("Total documents:", len(docs))

    if docs:
        print("Sample document:", docs[0])