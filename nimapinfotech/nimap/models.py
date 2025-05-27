
from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    clientName = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    createdBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="clients")

    def __str__(self):
        return self.clientName

class Project(models.Model):
    projectName = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    users = models.ManyToManyField(User, related_name='projects')
    createdAt = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="createdProjects")

    def __str__(self):
        return self.projectName

