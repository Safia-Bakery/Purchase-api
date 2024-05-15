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