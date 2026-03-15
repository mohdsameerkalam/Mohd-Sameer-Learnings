from fastapi import FastAPI, Path,HTTPException, Query

import json

app=FastAPI()
#loading json files
def load_data():
    with open('file.json','r') as f:
        data=json.load(f)
    return data

#SGI - server gateway interface (type wsgi[at a time one rqst] & asgi[a-asynchronous, can process multiple rqst at a time/parallel processing ])
#it enables a two way communication between web server and api
#fastapi uses asgi
 
@app.get("/")
def learning():
    return {"message":"Welcome shoeib gandu"}

@app.get("/data")#@ is called decorator
def view():
    data=load_data()
    return data
#calling specific data from json

# -------------------------------------------------------------------------
# About Path parameters in FastAPI:
# - What: Path parameters let you capture values from the URL path (like /data/{patientid}) and use them in your endpoint functions.
# - Why: They make your API dynamic, allowing you to fetch or process data based on user input directly from the URL.
# - How: Define them in your route with curly braces {} and receive them as function arguments.
# - Example usage:
#     @app.get("/items/{item_id}")
#     def read_item(item_id: int = Path(..., description="The ID of the item to get")):
#         return {"item_id": item_id}

@app.get("/data/{patientid}")#passing parameter patient id
def patient(patientid: str = Path(...,description="id of the employee")): #path is used to add description and ... means this field is required
    data=load_data()
    if(patientid in data):
        return data[patientid]
        # Raise an HTTPException with status code 404 if the patient ID is not found.
    # This sends a proper error response to the client instead of returning a regular dictionary.
    raise HTTPException(status_code=404, detail="Patient not found")  # to add http exceptions like error404 etc

# -------------------------------------------------------------------------
# About HTTPException in FastAPI:
# - What: HTTPException lets you send proper HTTP error responses (like 404, 400, etc.) from your API endpoints.
# - Why: Instead of just returning a dictionary for errors, raising HTTPException makes sure the client gets the right HTTP status code and a clear error message.
# - Types: You can use HTTPException for any HTTP status code, such as:
#     - 404 (Not Found)
#     - 400 (Bad Request)
#     - 401 (Unauthorized)
#     - 403 (Forbidden)
#     - 422 (Unprocessable Entity)
#     - 500 (Internal Server Error)
# - Example usage:
#     raise HTTPException(status_code=404, detail="Item not found")


# -------------------------------------------------------------------------
# About Query parameters in FastAPI:
@app.get("/sort")
def sort_patients(sort_by: str = Query(...,description="sort on the basis of marks"), order: str = Query('asc',description="ascending order")):
    valid_fields = ["marks"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400)
    if order not in ['asc','desc']:
        raise HTTPException(status_code=404)
    data=load_data()
    sorted_data=sorted(data.values(), key =lambda x: x.get(sort_by,0),reverse=False)
    return sorted_data
# - What: Query parameters are values you pass in the URL after a '?' (like /items?name=apple&price=10).
# - Why: They let users filter, search, or customize the data they get from your API without changing the URL path.
# - How: Just add function arguments that aren't part of the path. FastAPI automatically treats them as query parameters.
# - Example usage:
#     @app.get("/items/")
#     def read_items(name: str = None, price: int = None):
#         # Access name and price from the query string, e.g. /items?name=apple&price=10
#         return {"name": name, "price": price}
# - Extra: You can use Query from fastapi to add descriptions, set defaults, and add validation:
#     from fastapi import Query
#     @app.get("/search/")
#     def search(q: str = Query(..., min_length=3, description="Search term")):
#         return {"query": q}
# -------------------------------------------------------------------------
 