from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    client = serializers.StringRelatedField()
    createdBy = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = ['id', 'projectName', 'client', 'users', 'createdAt', 'createdBy']

class ProjectCreateSerializer(serializers.Serializer):
    projectName = serializers.CharField(max_length=100)
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

class ClientSerializer(serializers.ModelSerializer):
    createdBy = serializers.StringRelatedField()
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'clientName', 'createdAt', 'updatedAt', 'createdBy', 'projects']
