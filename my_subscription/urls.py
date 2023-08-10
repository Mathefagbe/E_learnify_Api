from django.urls import path as url
from .views import (MyLearningApiView,AutoAddLessonCompleteApiView)


urlpatterns = [
    url('mylearning/',MyLearningApiView.as_view(),name='mylearning'),
    url('mylearning/lesson/<uuid:id>/completed/',AutoAddLessonCompleteApiView.as_view(),name='completed_lesson'),
]