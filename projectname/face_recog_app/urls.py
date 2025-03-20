from django.urls import path
from .views import home_view, face_recognition_view 

urlpatterns = [
    path('', home_view, name='home'),
    path('recognize/', face_recognition_view, name='face_recognition'),
]
