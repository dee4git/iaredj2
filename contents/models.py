from django.contrib.auth.models import User
from django.db import models

levels = [
    ('CEO', 'CEO'),
    ('CTO', 'CTO'),
    ('Executive', 'Executive'),
    ('Researcher', 'Researcher'),
]


# Create your models here.
class Staff(models.Model):
    name = models.CharField(max_length=50, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    research_interest = models.CharField(max_length=10000, blank=True)
    designation = models.CharField(max_length=100, default='Researcher')
    level = models.CharField(max_length=100, choices=levels, default='Junior')
    phone = models.CharField(max_length=11, unique=True, blank=True, null=True)
    linked_in = models.URLField(max_length=1000, blank=True)
    github = models.URLField(max_length=999, blank=True)
    photo = models.ImageField(upload_to='media/team')
    about = models.TextField(max_length=1000, null=True,blank=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_fields(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Staff._meta.fields]


class WhitePaper(models.Model):
    tittle = models.CharField(max_length=1000, null=False, default='Tittle goes here')
    tags = models.CharField(max_length=1000, null=True)
    authors = models.CharField(max_length=1000, null=True)
    doi = models.URLField(max_length=1000, blank=True, null=True)
    pdf = models.FileField(null=False, upload_to='media/white-papers')
    hidden = models.BooleanField(default=False)


class SolutionCategory(models.Model):
    name = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='media/solution-category')
    description = models.TextField(max_length=10000)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Solution(models.Model):
    name = models.CharField(max_length=100)
    solution_category = models.ForeignKey(SolutionCategory, on_delete=models.SET_NULL, null=True)
    cover = models.ImageField(upload_to='media/solution')
    description = models.TextField(max_length=10000)
    hidden = models.BooleanField(default=False)
