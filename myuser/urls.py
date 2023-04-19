from django.urls import path
from . import views

app_name='myuser'

urlpatterns = [
    path('edit/' , views.edit , name='edit'),
]
