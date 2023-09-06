from django.urls import path as url
from .views import (MyLearningApiView,AutoAddLessonCompleteApiView,EnrollApiView)


urlpatterns = [
    url('mylearning/',MyLearningApiView.as_view(),name='mylearning'),
    url('course/<uuid:id>/enroll/',EnrollApiView.as_view(),name='enroll'),
    url('mylearning/lesson/<uuid:id>/completed/',AutoAddLessonCompleteApiView.as_view(),name='completed_lesson'),
]