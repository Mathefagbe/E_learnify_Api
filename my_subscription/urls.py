from django.urls import path as url
from .views import (MyLearningApiView,AutoAddLessonCompleteApiView,EnrollApiView,OnGoingDetail,CompletedCourse)


urlpatterns = [
    url('mylearning/',MyLearningApiView.as_view(),name='mylearning'),
    url('course/<uuid:id>/enroll/',EnrollApiView.as_view(),name='enroll'),
    url('mylearning/lesson/<uuid:id>/completed/',AutoAddLessonCompleteApiView.as_view(),name='completed_lesson'),
    url('ongoing_course/<uuid:id>/',OnGoingDetail.as_view(),name='ongoing_course'),
     url('completed/course/',CompletedCourse.as_view(),name='completed_course'),
]