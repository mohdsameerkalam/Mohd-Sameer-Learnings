from pydantic import BaseModel
from typing import Optional, List,Dict 

#python don't have by default typevalidation so pydantic helps to overcome this problem

# step1-  define a pydantic model that represents the ideal schema of model
        #this includes the expected fields, their types and any validation constraints

# step2- Instantiate the model with raw input data (usually a dictionary or json like structure)
        #pydantic will automatically validate the data and correct it into correct python types(if possible)
        #if the data doesn't meet the models requirements, pydantic will   raise a value error

# step3- Pass the validated model object to functions or use it throughout your codebase
        #This ensures that every part of your program works with clean, type-safe, and logically valid data


#creating base model for pydantic
class Patient(BaseModel):
    name:str  
    age:int
    weight:Optional[float]=None
    married:bool
    contact: Dict[str,str]#type dictionary where key value are str type
    allergies: Optional[list[str]]=None# list of str but not required field it's optional


#rest code
def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)

name =input("enter your name")
age=int(input("enter your age"))
weight=float(input("enter your weight"))
married=input("enter your married").lower() =="true"
contact=eval(input("enter your contact"))
allergies=input("enter your allergies")
allergiesa = [a.strip() for a in allergies.split(",")] if allergies else None

patient_info = {"name":name, "age":age, "weight":weight,"married": married,"contact":contact,"allergies":allergiesa}
patient1 = Patient(**patient_info)

update_patient_data(patient1)