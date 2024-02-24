from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator


from django.db import models

class Author(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    total_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, validators=[MaxValueValidator(5.00)])

    def __str__(self):
        return self.name
    
    @property
    def total_ratings(self):
        
        return self.total_rating
    

class Reader(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name='book')
    total_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, validators=[MaxValueValidator(5.00)])

    def __str__(self):
        return self.title
    
    @property
    def total_ratings(self):
        
        return self.total_rating



class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    review = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, validators=[MaxValueValidator(5.00)])
    

    def save(self, *args, **kwargs):
        
        if self.author:
            print("heloooo")
            print(type(self.rating))
            print(type(self.author.total_rating))
            if float(self.author.total_rating)>0.0:
                self.author.total_rating = (float(self.author.total_rating) + float(self.rating)) / 2
            else:
                self.author.total_rating = (float(self.author.total_rating) + float(self.rating))
            self.author.save()
        elif self.book:
            if float(self.book.total_rating)>0.1:
                self.book.total_rating = (float(self.book.total_rating) + float(self.rating)) / 2
            else:
                self.book.total_rating = (float(self.book.total_rating) + float(self.rating))
            self.book.save()
        super(Review, self).save(*args, **kwargs)

    def __str__(self):
        return f"Review for {self.author.name if self.author else self.book.title}"
