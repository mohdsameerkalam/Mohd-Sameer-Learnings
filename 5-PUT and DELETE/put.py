# create  a pydantic model
# validate data
# update
from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
import os

app = FastAPI()

FILE_NAME = "post_file.json"


# =========================
# Utility Functions
# =========================

def load_data():
    if not os.path.exists(FILE_NAME):
        return {}
    with open(FILE_NAME, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)


# =========================
# Pydantic Models
# =========================

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of employee", examples=["E01"])]
    name: Annotated[str, Field(..., description="Name of the employee")]
    Roll_No: Annotated[int, Field(..., gt=0, description="Roll number of employee")]
    gender: Annotated[Literal["male", "female"], Field(..., description="Gender")]
    marks: Annotated[float, Field(..., gt=0, description="Marks")]

    @computed_field
    @property
    def cgpa(self) -> str:
        if self.marks < 4:
            return "fail"
        elif self.marks < 7:
            return "average"
        return "good"


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    Roll_No: Optional[int] = Field(default=None, gt=0)
    gender: Optional[Literal["male", "female"]] = None
    marks: Optional[float] = Field(default=None, gt=0)


# =========================
# Routes
# =========================

@app.get("/")
def home():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records"}


@app.get("/view")
def view_all():
    return load_data()


@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ...,
        description="ID of the patient in the DB",
        examples=["E1"]
    )
):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Return validated model (includes cgpa)
    patient = Patient(id=patient_id, **data[patient_id])
    return patient


# =========================
# CREATE
# =========================

@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    # Save without id (id is key)
    data[patient.id] = patient.model_dump(exclude={"id", "cgpa"})

    save_data(data)

    return {"message": "Patient created successfully"}


# =========================
# UPDATE
# =========================

@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_data = data[patient_id]

    # Merge old data with new data
    updated_data = {
        **existing_data,
        **patient_update.model_dump(exclude_unset=True)
    }

    try:
        # Validate full object
        validated_patient = Patient(id=patient_id, **updated_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Save without id and computed field
    data[patient_id] = validated_patient.model_dump(
        exclude={"id", "cgpa"}
    )

    save_data(data)

    return {"message": "Patient updated successfully"}


# =========================
# DELETE
# =========================

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]
    save_data(data)

    return {"message": "Patient deleted successfully"}
