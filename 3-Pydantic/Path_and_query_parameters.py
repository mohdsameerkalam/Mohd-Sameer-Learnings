#Parameters are the information sent to the api
# Path parameters are dynamic segments of a url path used to identify a specific resource
# Path(..., )  -> here the three dot means this is required  basic syntax -> Path(default, options...)


# Why Path() exists
# Path() lets you:
# Make the parameter required
# Add rules (validation)
# Improve Swagger docs
# Get automatic errors (no manual checks)


from fastapi import FastAPI, Path,HTTPException, Query

import json

app=FastAPI()
#loading json files
def load_data():
    with open('file.json','r') as f:
        data=json.load(f)
    return data

@app.get("/")
def learning():
    return {"message":"Welcome shoeib gandu"}

@app.get("/data")#@ is called decorator
def view():
    data=load_data()
    return data

#Path(..., gt=0) gt means greater than so value greater than 0
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description = "The id of the Patient", min_length=1)): #here we used path parameter
    #load all the patients
    data= load_data()

    if patient_id in data:
        return data[patient_id]
    return {'error': 'patient not found'}


# | Option                      | Use case / Example                   |
# | --------------------------- | ------------------------------------ |
# | `description`               | Shows info in `/docs`                |
# | `min_length` / `max_length` | Strings length validation            |
# | `gt`, `lt`, `ge`, `le`      | Numeric range validation             | gt greater than , le - leass or equal
# | `regex`                     | Pattern matching IDs (e.g., E1, E23) |



# Query Parameters
@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of roll no'), order: str = Query('asc', description = 'sort in asc or desc order')):
    valid_fields = ['Roll NO']

    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc or desc')
    
    data = load_data()
    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data