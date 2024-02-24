from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.AuthorCreateListAPIView.as_view()),
    path('author_create_list', views.AuthorCreateListAPIView.as_view()),
    path('reader_create_list', views.ReaderCreateListAPIView.as_view()),
    path('book_create',views.BookCreateListAPIView.as_view()),
    path('book_update/<int:pk>',views.BookUpdateApiView.as_view()),
    path('review_author_create',views.ReviewAuthApiView.as_view()),
    path('review_book_create',views.ReviewBookApiView.as_view()),
    path('authorvise_review/<int:author>',views.AuthorBasedReviewApiView.as_view())
]




