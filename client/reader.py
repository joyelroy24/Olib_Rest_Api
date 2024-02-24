import requests
from getpass import getpass

# Authenticate user
auth_endpoint='http://localhost:8000/login'
username=input("Enter YOur Username :")
password=getpass("Enter YOur Password :")
print(password)
auth_response=requests.post(auth_endpoint,json={'username':username,'password':password})



# if login success > user got option for view author or book
if auth_response.status_code==200:
    print("........Login Success........")
    token=auth_response.json()['token']
    option=int(input('enter 1 for view author,2 for view books :'))
    headers={
            "Authorization":f"Token {token}"
        }
    
    # get the author list and give to user
    if option==1:
        
        endpoint = "http://localhost:8000/author_create_list" 
        

        get_response = requests.get(endpoint,headers=headers) 
        print(".........Authors--------------")
        print(get_response.json())
        textfordisplay_review_authors=''

        # create a text identitfy author and pk to user input management
        
        print("**************")
        review_or_viewReviews=int(input("enter 1 for view reviews enter 2 add reviews :"))
        for i in get_response.json():
            text=f" Enter {i['pk']} for author {i['name']}, "
            textfordisplay_review_authors=textfordisplay_review_authors+text
        textfordisplay_review_authors=textfordisplay_review_authors+" : "

        # display the text with author and corresponding id's to enter input from user
        # ;here user will enter pk of author using that we can view author specifc reviews
        reviews_about_author=int(input(textfordisplay_review_authors)) 

        if review_or_viewReviews==1:
            endpoint = "http://localhost:8000/authorvise_review/" 
            # add pk of user to endpont
            endpoint=endpoint+str(reviews_about_author)
            get_response = requests.get(endpoint,headers=headers) 
            print("...........Reviews............... \n ")
            print(get_response.json())
            
        else:
            # option for add review 
            review=input("enter review :")
            rate=int(input("enter rate out of 5 :"))
            endpoint = "http://localhost:8000/review_author_create" 
            
            
        
            get_response = requests.post(endpoint,headers=headers,json={"review":review,'rating':rate,'author':reviews_about_author}) 
                
            if auth_response.status_code==200:
                print("....Review Added.....")
                
                print(get_response.json())   
            
                
    elif option==2:
        
        # dispply books list to user
        endpoint = "http://localhost:8000/book_create"
             
        get_response = requests.get(endpoint,headers=headers) 
        print("...........Our Books............... \n ")
        print(get_response.json()) 
        
        get_response = requests.get(endpoint,headers=headers) 

        print(get_response.json())
        # create a text with book title and book id for user input action
        
        textfordisplay_review_book=''
        for i in get_response.json():

            text=f" Enter {i['pk']} for book {i['title']}, "
            textfordisplay_review_book=textfordisplay_review_book+text
        textfordisplay_review_authors=textfordisplay_review_book+" : "
        print("***************")
        # display text contant book title and id, to get input from user 
        reviews_about_book=int(input(textfordisplay_review_book)) 

        review=input("enter review :")
        rate=int(input("enter rate out of 5 :"))
        endpoint = "http://localhost:8000/review_book_create" 
        
        
    
        get_response = requests.post(endpoint,headers=headers,json={"review":review,'rating':rate,'book':reviews_about_book}) 
            
        if auth_response.status_code==200:
            print("....Review Added.....")
            
            print(get_response.json())   
        
