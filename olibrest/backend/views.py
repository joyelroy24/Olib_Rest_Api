from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import mixins,generics,authentication
from .models import Author,Reader,Book,Review
from .serializers import AuthorSerializer,ReaderSerializer,BookSerializer,ReviewBookSerializer,ReviewAuthSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.


# for author list,author create
class AuthorCreateListAPIView(mixins.CreateModelMixin,mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    

    def get(self,request,*args,**kwargs):
        print(request.user)
        print("workinggggg get")
        return self.list(request,*args,**kwargs)

    def post(self, request, *args, **kwargs):
        print("workinggggg")
        return self.create(request, *args, **kwargs)
    
#  for create reader, list readers
class ReaderCreateListAPIView(mixins.CreateModelMixin,mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
    

    def get(self,request,*args,**kwargs):
        print("workinggggg get")
        return self.list(request,*args,**kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

# fro create book, list books
class BookCreateListAPIView(mixins.CreateModelMixin,mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field='pk'
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):  
                    
        return self.list(request, *args, **kwargs)
    

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    
    
# for update books 
class BookUpdateApiView(mixins.UpdateModelMixin,mixins.RetrieveModelMixin,generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field='pk'
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

    # check for owner book try to update
    def get(self,request,*args,**kwargs):
        print(args,kwargs)
        pk=kwargs.get('pk')
     
        isauthor=Author.objects.filter(user=request.user).exists()
        if isauthor:
            author=Author.objects.get(user=request.user)
            isauthorof_boook=Book.objects.filter(pk=pk,author=author).exists()
            if not isauthorof_boook:
                return Response(
                    {"detail": "Only Authorized Author can Add books."},
                    status=status.HTTP_403_FORBIDDEN,)
           
            return self.retrieve(request,*args,**kwargs)
        return Response(
                    {"detail": "Only Authorized Author can Update book."},
                    status=status.HTTP_403_FORBIDDEN,)
    

    def put(self,request,*args,**kwargs):
        print("puttt")
        pk=kwargs.get('pk')
        isauthor=Author.objects.filter(user=request.user).exists()
        if isauthor:
            author=Author.objects.get(user=request.user)
            print(author)
            isauthorof_boook=Book.objects.filter(pk=pk,author=author).exists()
            if not isauthorof_boook:
                return Response(
                    {"detail": "Only Authorized Author can Update books."},
                    status=status.HTTP_403_FORBIDDEN,)
           
            return self.update(request,*args,**kwargs)
        return Response(
                    {"detail": "Only Authorized Author can Update book."},
                    status=status.HTTP_403_FORBIDDEN,)
        
    


# for review author, list reviews of author
class ReviewAuthApiView(mixins.CreateModelMixin,mixins.ListModelMixin,generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewAuthSerializer
    lookup_field='pk'
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self,request,*args,**kwargs):
        
        return self.list(request,*args,**kwargs)

# for review books,list book reviews
class ReviewBookApiView(mixins.CreateModelMixin,mixins.ListModelMixin,generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewBookSerializer
    lookup_field='pk'
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self,request,*args,**kwargs):
        
        return self.list(request,*args,**kwargs)
    
    
# view reviews author wise
class AuthorBasedReviewApiView(mixins.ListModelMixin,generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewAuthSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # lookup_field='pk'

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

    def get(self,request,*args,**kwargs):
        print(args,kwargs)
        print(request.user)
        author=kwargs.get('author')
        if author!=None:
            queryset=Review.objects.filter(author=author)
            data=ReviewAuthSerializer(queryset,many=True).data
            return Response(data)    
        


        