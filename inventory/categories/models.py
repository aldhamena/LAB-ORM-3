from django.db import models

# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=1024)
    description = models.TextField()

    def __str__(self) -> str:
        return f"{self.name}"