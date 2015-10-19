from django.db import models

# Create your models here.
class Lot(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name