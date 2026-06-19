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

@router.get("/area/update")
async def update_area():
    query = {"area_type": "upazila"}
    
    cursor = areas_collection.find(query)
    
    data = []
    async for document in cursor:
        document["_id"] = str(document["_id"]) 
        data.append(document)
    
    return {
        "data": data
    }    
