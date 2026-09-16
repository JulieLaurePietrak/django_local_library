from django.urls import path
from . import views

# The path() function defines the following:

# A URL pattern, which is an empty string: ''. We'll discuss URL patterns in detail when working on the other views.
# A view function that will be called if the URL pattern is detected: views.index, which is the function named index() in the views.py file.

urlpatterns = [
    path('', views.index, name='index'),
]