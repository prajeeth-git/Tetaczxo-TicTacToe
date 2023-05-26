from django.db import models

# Create your models here.
class gameroom(models.Model):
    def __str__(self):
        return f"{self.id}"