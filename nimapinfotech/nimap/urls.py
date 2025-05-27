from django.urls import path
from .views import ClientAPI, CreateProjectAPI, UserProjectsAPI, ClientWithProjectsAPI

urlpatterns = [
    path('clients/', ClientAPI.as_view(), name='client_api'),
    path('projects/create/', CreateProjectAPI.as_view(), name='create_project'),
    path('projects/user/', UserProjectsAPI.as_view(), name='user_projects'),
    path('client/with-projects/', ClientWithProjectsAPI.as_view(), name='client-with-projects'),
]
