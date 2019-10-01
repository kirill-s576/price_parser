from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=50)
    usef_full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username+" \ "+self.usef_full_name
