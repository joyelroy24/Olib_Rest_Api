import requests
from getpass import getpass

# check for who is goining to register 
profile=int(input('Enter 1-Author , Enter 2 for Reader '))
# create author
if profile==1:
    authcreate_endpoint='http://localhost:8000/author_create_list'
    username=input("Enter YOur Username :")
    password=getpass("Enter YOur password :")
    name=input("Enter Your name :")
    print(password)
    auth_response=requests.post(authcreate_endpoint,json={'username':username,'password':password,'name':name})

    print(auth_response.json())
    if auth_response.status_code==200:
        print("Login Sucsess")

# create reader
if profile==2:
    authcreate_endpoint='http://localhost:8000/reader_create_list'
    username=input("Enter YOur Username :")
    password=getpass("Enter YOur password :")  
    name=input("Enter Your name :")
    print(password)
    auth_response=requests.post(authcreate_endpoint,json={'username':username,'password':password,'name':name})

    print(auth_response.json())
    