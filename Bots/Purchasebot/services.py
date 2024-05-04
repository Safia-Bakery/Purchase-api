def transform_list(lst, size, key):
    # if key=='id':
    
    #     return [[f"{item.id}" for item in lst[i:i+size]] for i in range(0, len(lst), size)]
    if key=='id':
        return [[f"{item.id}" for item in lst[i:i+size]] for i in range(0, len(lst), size)]