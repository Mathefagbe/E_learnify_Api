from django.urls import path as url
from .views import (CoursesApiView,CreateReviewApiView,SubCourseApiView,ReviewApiView,
                    CatgoryCoursesApiView,CategoryApiView,CoursesDetailApiView,AboutCourseApiView,RecentCourse,PopularCourse
                    )


urlpatterns = [
    url('courses/',CoursesApiView.as_view(),name='course_list'),
    url('courses/popular/',PopularCourse.as_view(),name='course_list'),
    url('courses/recent/',RecentCourse.as_view(),name='course_list'),
    # url('course/create/',CreateCoursesApiView.as_view(),name='course_create'),
    url('course/<uuid:id>/',CoursesDetailApiView.as_view(),name='course_detail'),
    url('course/<uuid:id>/reviews/',ReviewApiView.as_view(),name='list_reviews'),
    url('course/<uuid:id>/review/create/',CreateReviewApiView.as_view(),name='create_review'),
    url('course/<uuid:id>/subcourse/',SubCourseApiView.as_view(),name='lesson_list'),
    url('category/',CategoryApiView.as_view(),name='category_list'),
    url('course/<uuid:id>/about/',AboutCourseApiView.as_view(),name='about_course'),
    url('category/<id>/courses/',CatgoryCoursesApiView.as_view(),name='category_course_list'),
]