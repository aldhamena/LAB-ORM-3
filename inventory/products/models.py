from django.db import models
from suppliers.models import Supplier

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):

    class RatingChoices(models.IntegerChoices):
        STAR1 = 1, "One Star"
        STAR2 = 2, "Two Stars"
        STAR3 = 3, "Three Stars"
        STAR4 = 4, "Four Stars"
        STAR5 = 5, "Five Stars"

    title = models.CharField(max_length=1024)
    description = models.TextField()
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True)
    rating = models.SmallIntegerField(choices=RatingChoices.choices)
    production_date = models.DateField()
    poster = models.ImageField(upload_to="images/", default="images/default.jpg")
    categories = models.ManyToManyField(Category)



    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    rating = models.SmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f"{self.name} on {self.product.title}"
