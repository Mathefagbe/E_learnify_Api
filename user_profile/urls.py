from django.urls import path as url
from .views import InstructorProfileApiView,UserProfileApiView


urlpatterns = [
    url('profile/<id>',InstructorProfileApiView.as_view(),name='retrive_instructor'),
    url('profile/',UserProfileApiView.as_view(),name='retrive_user'),
    # url('profile/create',UserProfileCreateApiView.as_view(),name='create_user'),
    
]