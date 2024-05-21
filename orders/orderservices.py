from datetime import datetime
import pytz
timezonetash = pytz.timezone("Asia/Tashkent")

import requests
from dotenv import load_dotenv
import os
import xml.etree.ElementTree as ET
load_dotenv()

BASE_URL = os.getenv("BASE_URL")




def find_hierarchy(data, parent_id):
    def dfs(current_id):
        result = []
        for item in data:
            if item["parent"] == current_id:
                child_id = item["id"]
                result.append({
                    "id": child_id,
                    "name": item["name"],
                    "num":item['num'],
                    'code':item['code'],
                    "parent":item["parent"],
                    "category":item["category"],
                    "description":item["description"]
                })
                result.extend(dfs(child_id))  # Recursive call for children
        return result

    # Find the parent item
    parent_item = next((item for item in data if item["id"] == parent_id), None)

    if parent_item:
        return [{
            "id": parent_id,
            "name": parent_item["name"],
            "num":parent_item['num'],
            'code':parent_item['code'],
            "parent":parent_item["parent"],
            "category":parent_item["category"],
            "description":parent_item["description"]
        }] + dfs(parent_id)
    else:
        return []



def get_prices(key,department_id):
    current_date = datetime.now(timezonetash).strftime("%Y-%m-%d")
    prices = requests.get(f"{BASE_URL}/resto/api/v2/reports/balance/stores?timestamp={current_date}&department={department_id}&key={key}")
    return prices.json()




def get_productsmainunit(key):
    products = requests.get(f"{BASE_URL}/resto/api/v2/products?key={key}")
    products = ET.fromstring(products.content)
    products = products.findall("productDto")
    return products








