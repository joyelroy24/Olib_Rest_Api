import requests
from getpass import getpass

# autenticate 
auth_endpoint='http://localhost:8000/login'
username=input("Enter YOur Username :")
password=getpass("Enter YOur Password :")
print(password)
auth_response=requests.post(auth_endpoint,json={'username':username,'password':password})

print(auth_response.json())

# if login success can >  create books
if auth_response.status_code==200:
    print("........Login Success........")
    token=auth_response.json()['token']
    
    headers={
            "Authorization":f"Token {token}"
        }
    
    title=input("Enter Book title :")

    endpoint = "http://localhost:8000/book_create" 
         
    get_response = requests.post(endpoint,headers=headers,json={'title':title}) 

    if auth_response.status_code==200:
        print("....Book Added.....")
                
        print(get_response.json())
    
       