from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer, ProjectCreateSerializer


# Replaces ClientViewSet
class ClientAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client_id = request.data.get('id', None)
        if client_id:
            try:
                client = Client.objects.get(id=client_id)
                serializer = ClientSerializer(client)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Client.DoesNotExist:
                return Response({'msg': 'Client with this ID not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            clients = Client.objects.all()
            serializer = ClientSerializer(clients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(createdBy=request.user)
            return Response({'msg': 'Client created successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'msg': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        client_id = request.data.get('id', None)
        if client_id:
            try:
                client = Client.objects.get(id=client_id)
                serializer = ClientSerializer(client, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg': 'Client updated successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)
                return Response({'msg': 'Invalid update data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            except Client.DoesNotExist:
                return Response({'msg': 'Client with this ID not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': 'Please provide a client ID'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        client_id = request.data.get('id', None)
        if client_id:
            try:
                client = Client.objects.get(id=client_id)
                client.delete()
                return Response({'msg': 'Client deleted successfully!'}, status=status.HTTP_200_OK)
            except Client.DoesNotExist:
                return Response({'msg': 'Client with this ID not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': 'Please provide a client ID'}, status=status.HTTP_400_BAD_REQUEST)


# Replaces CreateProjectForClient
class CreateProjectAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        client_id = request.data.get('client_id')
        if not client_id:
            return Response({'msg': 'client_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({'msg': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid():
            project = Project.objects.create(
                projectName=serializer.validated_data['projectName'],
                client=client,
                createdBy=request.user
            )
            project.users.set(serializer.validated_data['users'])
            project.save()
            output_serializer = ProjectSerializer(project)
            return Response({'msg': 'Project created successfully', 'data': output_serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'msg': 'Invalid project data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Replaces UserProjectsView
class UserProjectsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(users=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClientWithProjectsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client_id = request.query_params.get('id')  # using query params for GET
        if not client_id:
            return Response({'msg': 'Please provide a client ID as ?id='}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({'msg': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

        # Fetch all projects linked to this client
        projects = Project.objects.filter(client=client)

        client_data = ClientSerializer(client).data
        projects_data = ProjectSerializer(projects, many=True).data

        return Response({
            'client': client_data,
            'projects': projects_data
        }, status=status.HTTP_200_OK)
