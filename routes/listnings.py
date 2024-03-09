import json, os
from fastapi import APIRouter, Depends, Request, status, HTTPException
from models.listning import Listning, Parameters
from config.db import mongo_conn
from schemas.listning import listningEntity, listningsEntity

import os

cwd = os.getcwd()
listnings = APIRouter()
with open(cwd + '/config/orase.json', 'r') as file:
        coduri_orase = json.load(file)

orase = []
for judet in coduri_orase:
        orase.append(judet.get("region_name", ""))

def check_for_what(for_what):
    if for_what=="de_vanzare":
        return mongo_conn.anunturi.de_vanzare
    elif for_what=="de_inchiriat":
        return mongo_conn.anunturi.de_inchiriat
    else:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=for_what + " it is not defined in the database",
        )

def check_city(city):
    if city not in orase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=city + " it is not in our database",
        )

def check_query(query):
    new_dict = {}
    keys_to_remove = []

    for key, value in query.items():
        if value == '':
            keys_to_remove.append(key)
        else:
            new_dict[key] = value

    for key in keys_to_remove:
        del query[key]
    
    return query

@listnings.get("/api/v1/{for_what}/", tags=["Main"])
async def find(for_what,req: Request, params: Parameters.param = Depends()):
    db = check_for_what(for_what)
    query = {
         "camere": params.camere,
         "platforma":params.platforma,
         "price": { "$gt" : params.from_price, "$lte" : params.to_price}
        }
    sorting = params.sort
    sort_field=""
    sort_type=1
    # I will have those options: newly_created(default), lowest_price, highest_price
    if sorting == "":
        sort_field = "created_time"
        sort_type = -1
    elif sorting =="lowest_price":
        sort_field = "price"
        sort_type = 1
    elif sorting =="highest_price":
        sort_field = "price"
        sort_type = -1
    
    query = check_query(query)
    base_url = req.url._url.split("/api/v1/")[0]
    print(query)
    to_return = listningsEntity(db.find(query).sort(sort_field,sort_type).skip(params.skip).limit(params.lenght),for_what,base_url,params)

    return to_return

@listnings.get("/api/v1/{for_what}/{city}/", tags=["Main"])
async def find_by_city(for_what, city,req: Request, params: Parameters.param = Depends()):
    db = check_for_what(for_what)
    check_city(city)
    query = {
         "city": city,
         "camere": params.camere,
         "platforma":params.platforma,
         "price": { "$gt" : params.from_price, "$lte" : params.to_price}
        }
    sorting = params.sort
    sort_field=""
    sort_type=1
    # I will have those options: newly_created(default), lowest_price, highest_price
    if sorting == "":
        sort_field = "created_time"
        sort_type = -1
    elif sorting =="lowest_price":
        sort_field = "price"
        sort_type = 1
    elif sorting =="highest_price":
        sort_field = "price"
        sort_type = -1
    
    query = check_query(query)
    base_url = req.url._url.split("/api/v1/")[0]
    print(query)
    to_return = listningsEntity(db.find(query).sort(sort_field,sort_type).skip(params.skip).limit(params.lenght),for_what,base_url,params,city)

    return to_return
