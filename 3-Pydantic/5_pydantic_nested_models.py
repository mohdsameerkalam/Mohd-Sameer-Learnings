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

patient_dict = {'name':'Sam', 'gender':'Male', 'age':'24', 'address': address1}
patient1 = Patient(**patient_dict)

print(patient1)
print(patient1.name)
print(patient1.age)
print(patient1.gender)
print(patient1.address)
print(patient1.address.state)
print(patient1.address.city)
print(patient1.address.pin)



# better organization of related data
# resusability
# readability
# automatic validated no extra work needed 