from pydantic import BaseModel

class Address(BaseModel):
    city:str
    state:str
    pin: str
class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address
    # address can be mixup of alphanumeric etc we need to extract any single part like pin code so we use another class for such type

address_dict = {'city':'Lucknow', 'state':'Uttar Pradesh', 'pin':'226003'}
address1 = Address(**address_dict)
#exlude_unset=true   -> the thing whose object is not created will not be imported
patient_dict = {'name':'Sam', 'gender':'Male', 'age':'24', 'address': address1}
patient1 = Patient(**patient_dict)

# serialization is the process of converting a validated model instance into a standard Python dictionary or a JSON-formatted string.
# This allows Pydantic models to be easily stored, logged, or transmitted over a network, such as in a web API response.

temp1 = patient1.model_dump(exclude=['name','gender'])#for state in address exclude={'address':[state]}
temp2 = patient1.model_dump(include=['name','gender'])

print(temp1)
print(temp2)
print(type(temp2))

# output:

# {'age': 24, 'address': {'city': 'Lucknow', 'state': 'Uttar Pradesh', 'pin': '226003'}}
# {'name': 'Sam', 'gender': 'Male'}
# <class 'dict'>

