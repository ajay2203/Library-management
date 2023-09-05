from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    quantity = models.PositiveIntegerField(default=0)

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
