import csv
from pathlib import Path
from fastapi import APIRouter
from ..database import areas_collection

router = APIRouter()

@router.get("/area")
async def get_area():
    data_dir = Path(__file__).parents[2] / "data"

    with open(data_dir / "district.csv", newline="", encoding="utf-8") as f:
        districts = list(csv.DictReader(f))
    
    for row in districts:
        await areas_collection.insert_one({
            "area_parent_id": None,
            "area_type": "district",
            "area_name_en": None,
            "area_name_local": row["জেলা"],
            "district_id": int(row["district_id"])
        })

    # return {
    #     "message": f"Inserted {len(districts)} districts"
    # }    

    with open(data_dir / "upozila.csv", newline="", encoding="utf-8") as f:
        upazilas = list(csv.DictReader(f))
   

    for row in upazilas:
        await areas_collection.insert_one({
            "area_parent_id": None,
            "area_type": "upazila",
            "area_name_en": None,
            "area_name_local": row["উপজেলা"],
            "district_id": int(row["district_id"]),
            "upozila_id": int(row["upozila_id"]),
        })

    # return {
    #     "message": f"Inserted {len(upazilas)} upazilas"
    # }

    with open(data_dir / "union.csv", newline="", encoding="utf-8") as f:
        unions = list(csv.DictReader(f))

    for union_id, row in enumerate(unions, start=1):
        await areas_collection.insert_one({
            "union_id": union_id,
            "area_parent_id": None,
            "area_type": "union",
            "area_name_en": None,
            "area_name_local": row["ইউনিয়ন"],
            "district_id": int(row["district_id"]),
            "upozila_id": int(row["upozila_id"]),
        })

    return {
        "message": f"Inserted {len(districts)} districts, {len(upazilas)} upazilas, and {len(unions)} unions"
    }

# @router.get("/area/update")
# async def update_area():
#     result_data = []
#     updated_count = 0

#     query = {"area_type": "upazila"}
#     cursor = areas_collection.find(query)

#     async for document in cursor:

#         if document.get("area_parent_id") is None:

#             parent_query = {
#                 "area_type": "district",
#                 "district_id": document.get("district_id")
#             }

#             parent_data = await areas_collection.find_one(parent_query)

#             if parent_data:
#                 await areas_collection.update_one(
#                     {"_id": document["_id"]},
#                     {"$set": {"area_parent_id": parent_data["_id"]}}
#                 )
#                 updated_count += 1

#                 document["area_parent_id"] = parent_data["_id"]

#         document["_id"] = str(document["_id"])

#         if document.get("area_parent_id"):
#             document["area_parent_id"] = str(document["area_parent_id"])

#         result_data.append(document)

#     return {
#         "updated_count": updated_count,
#         "data": result_data
#     } 

@router.get("/area/update")
async def update_area():
    result_data = []
    updated_count = 0

    query = {"area_type": "union"}
    cursor = areas_collection.find(query)

    async for document in cursor:

        if document.get("area_parent_id") is None:

            parent_query = {
                "area_type": "upazila",
                "upozila_id": document.get("upozila_id")
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
