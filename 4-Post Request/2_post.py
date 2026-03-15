from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json 

app = FastAPI()

#  Annotated is a way to: attach runtime metadata to types without changing how type checkers interpret them.

class Patient(BaseModel):
    # id: Annotated[str, field(..., description='ID of employee', examples=['E01'])]
    # name: Annotated[str, field(..., description='name of the employee')]
    # Roll_No: Annotated[int, field(..., description='roll no of employee')]
    # gender: Annotated[Literal['male','female'], field(..., description='gender of employee')]
    # #    change post_file.json add few fields
    # marks: Annotated[float, field(..., gt=0, description='Marks')]
    id: Annotated[str, Field(..., description='ID of employee', examples=['E01'])]
    name: Annotated[str, Field(..., description='name of the employee')]
    Roll_No: Annotated[int, Field(..., description='roll no of employee')]
    gender: Annotated[Literal['male','female'], Field(..., description='gender of employee')]
    marks: Annotated[float, Field(..., gt=0, description='Marks')]

    @computed_field
    @property
    def cgpa(self)->str:
        if self.marks<4:
            return 'fail'
        elif self.marks<7:
            return 'average'
        else:
            return 'good'
        
def load_data():
    with open('post_file.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('post_file.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.get("/")
def hello():
    return {'message':'Patient Management System API'}

@app.get('/about')
def about():
    return {'message':'A fully functional API to manage your patient records'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str= Path(..., description='ID of the patient in the DB', example='P001')):
    data =load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.post('/create')
def create_patient(patient: Patient):
    # load existing data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    
    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'patient created successfully'})