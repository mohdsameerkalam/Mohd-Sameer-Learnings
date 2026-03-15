#a request body is a proportion of a http request that contains data sent by the client to the server.
#It is typically used in http methods such as POST, or PUT to transmit structured data (e.g. JSON, XML, form-data) for the purpose of creating or updating resources on the server.
# The server parses the request body to extract the necessary information and performs the intended operations.


# steps are as follows
#  step 1
#   __________                __________
#  |          |              |          |        
#  | CLIENT   |------------->| SERVER   |
#  |__________| (POST(JSON)) |__________| 

#  step2  
#  Validate --> with the help of pydantic
# Step 3
#  json file -> new record add