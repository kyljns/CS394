from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User


class FamilyMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='family_member')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    parents = models.ManyToManyField('self', blank=True, related_name='children', symmetrical=False)  # Many-to-Many for parents

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('parent', 'Parent'),
        ('child', 'Child'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='child')

    def __str__(self):
        return f"{self.user.username} ({self.role})"
