def transform_inventory_record(record):

    sku = record["sku"]
    brand = record["brand"]
    product = record["product"]
    price = record["price"]
    org_id = record["org_id"]

    text = f"""
    {product} from brand {brand} with SKU {sku} costs {price} rupees.
    This product belongs to organisation {org_id}.
    """

    metadata = {
        "org_id": org_id,
        "brand": brand,
        "price": price,
        "sku": sku
    }

    return text.strip(), metadata