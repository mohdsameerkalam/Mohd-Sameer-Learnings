from pydantic import BaseModel, Field, AnyUrl, field_validator
from typing import Optional, List,Dict

 
#creating base model for pydantic
class Patient(BaseModel):
    name:str  
    age:int
    weight:Optional[float]=None
    married:bool=False 
    email: str
    contact: Dict[str,str]#type dictionary where key value are str type
    allergies: Optional[list[str]]=None# list of str but not required field it's optional , None written so that by default it fills none

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains= ['hdfc.com','icici.com']
        domain_name = value.split('@')[-1] #extract value after @
    
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        
        return value

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
email = input("Enter your Email")
contact=eval(input("enter your contact"))
allergies=input("enter your allergies")
allergiesa = [a.strip() for a in allergies.split(",")] if allergies else None

patient_info = {"name":name, "age":age, "weight":weight,"married": married,"email":email,"contact":contact,"allergies":allergiesa}
patient1 = Patient(**patient_info)

update_patient_data(patient1)