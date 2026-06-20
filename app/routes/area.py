import csv
import json
from pathlib import Path
from fastapi import APIRouter
from ..database import areas_collection, client

router = APIRouter()

@router.get("/area")
async def get_area():
    data_dir = Path(__file__).parents[2] / "data"

    with open(data_dir / "district.csv", newline="", encoding="utf-8") as f:
        districts = list(csv.DictReader(f))
    
    with open(data_dir / "upazila.csv", newline="", encoding="utf-8") as f:
        upazilas = list(csv.DictReader(f))

    with open(data_dir / "union.csv", newline="", encoding="utf-8") as f:
        unions = list(csv.DictReader(f))

    try:
        async with await client.start_session() as session:
            async with session.start_transaction():
                for row in districts:
                    await areas_collection.insert_one({
                        "area_parent_id": None,
                        "area_type": "district",
                        "area_name_en": None,
                        "area_name_local": row["জেলা"],
                        "district_id": int(row["district_id"])
                    }, session=session)

                for row in upazilas:
                    await areas_collection.insert_one({
                        "area_parent_id": None,
                        "area_type": "upazila",
                        "area_name_en": None,
                        "area_name_local": row["উপজেলা"],
                        "district_id": int(row["district_id"]),
                        "upazila_id": int(row["upazila_id"]),
                    }, session=session)

                for union_id, row in enumerate(unions, start=1):
                    await areas_collection.insert_one({
                        "union_id": union_id,
                        "area_parent_id": None,
                        "area_type": "union",
                        "area_name_en": None,
                        "area_name_local": row["ইউনিয়ন"],
                        "district_id": int(row["district_id"]),
                        "upazila_id": int(row["upazila_id"]),
                    }, session=session)
    except Exception as e:
        # Fallback for standalone MongoDB (no replica set)
        if "Transaction numbers are only allowed on a replica set member" in str(e):
            for row in districts:
                await areas_collection.insert_one({
                    "area_parent_id": None,
                    "area_type": "district",
                    "area_name_en": None,
                    "area_name_local": row["জেলা"],
                    "district_id": int(row["district_id"])
                })

            for row in upazilas:
                await areas_collection.insert_one({
                    "area_parent_id": None,
                    "area_type": "upazila",
                    "area_name_en": None,
                    "area_name_local": row["উপজেলা"],
                    "district_id": int(row["district_id"]),
                    "upazila_id": int(row["upazila_id"]),
                })

            for union_id, row in enumerate(unions, start=1):
                await areas_collection.insert_one({
                    "union_id": union_id,
                    "area_parent_id": None,
                    "area_type": "union",
                    "area_name_en": None,
                    "area_name_local": row["ইউনিয়ন"],
                    "district_id": int(row["district_id"]),
                    "upazila_id": int(row["upazila_id"]),
                })
        else:
            raise

    return {
        "message": f"Inserted {len(districts)} districts, {len(upazilas)} upazilas, and {len(unions)} unions"
    }

@router.get("/area/update/upazila")
async def update_area():
    result_data = []
    updated_count = 0

    query = {"area_type": "upazila"}
    cursor = areas_collection.find(query)

    async for document in cursor:

        if document.get("area_parent_id") is None:

            parent_query = {
                "area_type": "district",
                "district_id": document.get("district_id")
            }

            parent_data = await areas_collection.find_one(parent_query)

            if parent_data:
                await areas_collection.update_one(
                    {"_id": document["_id"]},
                    {"$set": {"area_parent_id": parent_data["_id"]}}
                )
                updated_count += 1

                document["area_parent_id"] = parent_data["_id"]

        document["_id"] = str(document["_id"])

        if document.get("area_parent_id"):
            document["area_parent_id"] = str(document["area_parent_id"])

        result_data.append(document)

    return {
        "updated_count": updated_count,
        "data": result_data
    } 

@router.get("/area/update/union")
async def update_area():
    result_data = []
    updated_count = 0

    query = {"area_type": "union"}
    cursor = areas_collection.find(query)

    async for document in cursor:

        if document.get("area_parent_id") is None:

            parent_query = {
                "area_type": "upazila",
                "upazila_id": document.get("upazila_id")
            }

            parent_data = await areas_collection.find_one(parent_query)

            if parent_data:
                await areas_collection.update_one(
                    {"_id": document["_id"]},
                    {"$set": {"area_parent_id": parent_data["_id"]}}
                )
                updated_count += 1

                document["area_parent_id"] = parent_data["_id"]

        document["_id"] = str(document["_id"])

        if document.get("area_parent_id"):
            document["area_parent_id"] = str(document["area_parent_id"])

        result_data.append(document)

    return {
        "updated_count": updated_count,
        "data": result_data
    } 

@router.get('/area/districts/json')
async def get_districts_json():

    data_dir = Path(__file__).parents[2] / "data"
    
    with open(data_dir / "districts.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    districts = data['districts']

    data_not_found = []
    for district in districts:
        #print(district['bn_name'])
        query = {"area_type": "district", "area_name_local": district['bn_name']}
        area = await areas_collection.find_one(query)
        if area:
            if area.get("area_name_en") is None:
                print(f"Updating district: {district['bn_name']} -> {district['name']}")
                await areas_collection.update_one(
                        {"_id": area["_id"]},
                        {"$set": {"area_name_en": district["name"]}}
                    )
        else:
            print(f"District not found: {district['bn_name']}")
            data_not_found.append(district['bn_name'])
        
    return {"data_not_found": data_not_found}

