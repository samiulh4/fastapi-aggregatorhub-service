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
            "area_name_en": None,
            "area_name_local": row["জেলা"],
            "parent_id": None,
            "source_id": int(row["district_id"])
        })

    with open(data_dir / "upozila.csv", newline="", encoding="utf-8") as f:
        upazilas = list(csv.DictReader(f))

    for row in upazilas:
        await areas_collection.insert_one({
            "area_name_en": None,
            "area_name_local": row["উপজেলা"],
            "parent_id": None,
            "source_id": int(row["district_id"])
        })

    return {
        "message": f"Inserted {len(districts)} districts and {len(upazilas)} upazilas"
    }
