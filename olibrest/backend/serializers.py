from rest_framework import serializers
from .models import Author, Reader, Book, Review
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth import authenticate


# author serializer with number of books SerializerMethodField
class AuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150,write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    number_of_books=serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Author
        fields = ['pk','username', 'password', 'name','total_ratings','number_of_books','pk']


    # defined what value should be returned in list for number of book field
    
  
    def create(self, validated_data):
        # create for create user and create author
        print(validated_data['username'])
        user_data = {
            'username': validated_data['username'],
            'password': validated_data['password'],
            'first_name': validated_data['name'],
        }
       
        user = User.objects.filter(username=validated_data['username']).first()
        if user is not None:
            if check_password(validated_data['password'],user.password):
                print("existtttttttttt")
                
                raise serializers.ValidationError("User with the same username and password already exists.")  
        
        user = User.objects.create_user(**user_data)

       
        del validated_data['username']
        del validated_data['password']
        

       
        author = Author.objects.create(user=user, name=validated_data['name'])
        return author



# reader serailizer
class ReaderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150,write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    

    class Meta:
        model = Reader
        fields = ['pk','username', 'password', 'name']

    # create for user account creation and reader
    def create(self, validated_data):
        
        print(validated_data['username'])
        user_data = {
            'username': validated_data['username'],
            'password': validated_data['password'],
            'first_name': validated_data['name'],
        }
       
        user = User.objects.filter(username=validated_data['username']).first()
        if user is not None:
            if check_password(validated_data['password'],user.password):
                print("existtttttttttt")
                
                raise serializers.ValidationError("User with the same username and password already exists.")  

        user = User.objects.create_user(**user_data)

       
        del validated_data['username']
        del validated_data['password']
        

       
        reader = Reader.objects.create(user=user, name=validated_data['name'])
        return reader

# Book serializer
class BookSerializer(serializers.ModelSerializer):
    Author=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Book
        fields = ['pk','title','Author','total_ratings']
    # create method only allowed for authorized user
    def create(self, validated_data):
        print("333333333333")
        request=self.context.get('request')
        
        existcheck=Author.objects.filter(user=request.user).exists()
        if not existcheck:
            raise serializers.ValidationError("Only Authorized Author can Add books.")
        else:
            author=Author.objects.get(user=request.user)
            validated_data['author']=author
        return super().create(validated_data)
    
    def get_Author(self,obj):
        if not isinstance(obj,Author):#check the object is an instance of product
            return None
        else:
            return obj.book.count()
        
        
# review author serailizer
class ReviewAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['author', 'review', 'rating']

        
    # check for already added review for same author by same user
    def create(self, validated_data):
    
        
        
        print(validated_data['author'])

        request=self.context.get('request')
        existcheck=Review.objects.filter(user=request.user,author=validated_data['author']).exists()
        if existcheck:
            raise serializers.ValidationError("Already Added review for this book.")
        
        validated_data['user'] = request.user
        return super().create(validated_data)
            

# review book serializer
class ReviewBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['book', 'review', 'rating']
    
    # check for already added review and rate for same book
    def create(self, validated_data):
        print("%%#@@@@@@@@@@@@@@")
        request=self.context.get('request')
        
        
        print(validated_data)
        print(validated_data['book'])

        existcheck=Review.objects.filter(user=request.user,book=validated_data['book']).exists()
        if existcheck:
            raise serializers.ValidationError("Already Added review for this book.")
        
        validated_data['user'] = request.user
        return super().create(validated_data)

            
