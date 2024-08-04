from django.db import models

# Create your models here.


class Supplier(models.Model):

    name = models.CharField(max_length=1024)
    description = models.TextField()
    logo = models.ImageField(upload_to="images/", default="images/default.jpg")

    def __str__(self) -> str:
        return f"{self.name}"