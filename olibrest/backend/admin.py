from django.contrib import admin
from .models import Author,Book,Reader,Review
# Register your models here.

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Reader)