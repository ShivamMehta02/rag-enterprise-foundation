import re

KNOWN_BRANDS = [
    "Technova",
    "UltraSys",
    "PrintCorp",
    "NetLink",
    "CoreSystems",
    "DisplayTech"
]

def extract_filters(user_query):

    brand = None
    price_limit = None

    # detect brand
    for b in KNOWN_BRANDS:
        if b.lower() in user_query.lower():
            brand = b

    # detect price like "under 6000"
    price_match = re.search(r"under\s+(\d+)", user_query)

    if price_match:
        price_limit = int(price_match.group(1))

    # remove filters from query text
    clean_query = user_query

    if brand:
        clean_query = clean_query.replace(brand, "")

    if price_limit:
        clean_query = re.sub(r"under\s+\d+", "", clean_query)

    clean_query = clean_query.strip()

    return clean_query, brand, price_limit