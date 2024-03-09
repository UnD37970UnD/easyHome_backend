import json


def listningEntity(item) -> dict:
    return {
        "id": str(item["id"]),
        "title": item["title"],
        "description": item["description"],
        "url": str(item["url"]),
        "created_time": item["created_time"],
        "photos": item["photos"],
        "location": item["location"],
        "price": item["price"],
        "currency": str(item["currency"]),
        "camere": str(item["camere"]),
        "negotiable": str(item["negotiable"]),
        "floor": item["floor"],
        "construction_date": item["construction_date"],
        "surface": item["surface"],
        "city": item["city"],
        "district": item["district"],
        "judet": item["judet"],
        "platforma": item["platforma"],
        "precise_location": item["precise_location"]
    }

def dict_to_link(base_url, param):
    dicti = json.loads(param.model_dump_json())
    dicti.pop("city")
    dicti["skip"] = dicti["skip"]+dicti["lenght"]
    query_string = '&'.join([f'{key}={value}' for key, value in dicti.items()])
    link = f'{base_url}?{query_string}'
    return link

def listningsEntity(entity,what_for,base_url,param,city=None) -> dict:
    if city == None:
        next_url = dict_to_link(base_url+"/api/v1/"+what_for+"/",param)
    else:
        next_url = dict_to_link(base_url+"/api/v1/"+what_for+"/"+city+"/",param)

    for_return = {
        "data" : [listningEntity(item) for item in entity],
        "info": {
            "next_url": next_url
        }
    }
    return for_return
