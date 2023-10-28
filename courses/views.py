from django.shortcuts import render,get_object_or_404
from .serializers import (CourseDetailOutputSerializer,ReviewSerializer,LessonOutputSerializer,
                          CategorySerializer,CourseOutputSerializer,SubCourseOutputSerializer,AboutCourseSerializer)
from rest_framework.generics import (ListAPIView,CreateAPIView,RetrieveAPIView)
from .models import Course,Review,Category,SubCourse,AboutCourse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import BasicAuthentication
from my_subscription.serializers import (EnrolledCourseDetailOutputSerializer,EnrollSubCourseOutputSerializer)
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from utils.error_handler import error_handler
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CourseFilters
from django.db.models import Avg,Sum
# from social_django.models
# Create your views here.

# apps views
class CoursesApiView(ListAPIView):
    serializer_class=CourseOutputSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]
    filter_backends=[filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['title','author__first_name','author__last_name']
    filterset_class=CourseFilters
    

    def get_queryset(self):
        return Course.objects.select_related('author',"category")\
            .prefetch_related("lessons","reviews",)\
                .annotate(avg_rating=Avg("reviews__rating"),total_lesson=Sum("lessons__duration")).all()
    
class PopularCourse(ListAPIView):
    serializer_class=CourseOutputSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]


    def get_queryset(self):
        return Course.objects.select_related('author',"category")\
            .prefetch_related("lessons","reviews",)\
                .annotate(avg_rating=Avg("reviews__rating"),total_lesson=Sum("lessons__duration")).order_by("-avg_rating").all()

class RecentCourse(ListAPIView):
    serializer_class=CourseOutputSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]

    def get_queryset(self):
        return Course.objects.select_related('author',"category")\
            .prefetch_related("lessons","reviews",)\
                .annotate(avg_rating=Avg("reviews__rating"),total_lesson=Sum("lessons__duration")).order_by("-date_created").all()

class CategoryApiView(ListAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]


class AboutCourseApiView(RetrieveAPIView):
    serializer_class=AboutCourseSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]
    lookup_field='id'


    def get_queryset(self):
        return AboutCourse.objects.select_related('course','course__author__instructor_profile',
                                                  'course__author__instructor_profile__instructor').\
            prefetch_related('course__lessons','requirements')\
                .annotate(total_duration=Sum("course__lessons__duration")).all()
    
    def get_object(self):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            obj = queryset.get(course__id=self.kwargs[self.lookup_field])
            self.check_object_permissions(self.request, obj)
        except Exception as e:
            data={
                "message":error_handler(e),
                "status":"failed"     
            }
            raise NotFound(data)
        return obj
    

class CoursesDetailApiView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]
    lookup_field='id'



    def get(self, request, *args, **kwargs):
        try:
            obj=Course.objects.select_related('author',"category").\
                prefetch_related('reviews')\
                    .annotate(avg_rating=Avg("reviews__rating"))\
                        .get(id=self.kwargs[self.lookup_field])
        
            self.check_object_permissions(self.request, obj)
            if self.request.user.enroll_courses.filter(id__in=[obj.id])\
                .prefetch_related("course__author__enroll_courses").exists():
                serializer=EnrolledCourseDetailOutputSerializer(obj,many=False,context={"request":self.request})
            else:
               serializer=CourseDetailOutputSerializer(obj,many=False,context={'request':self.request})
        except Exception as e:
            data={
                "message":error_handler(e),
                "status":"failed"     
            }
            raise NotFound(data)
        return Response(serializer.data)

# apps views
class CatgoryCoursesApiView(ListAPIView):
    serializer_class=CourseOutputSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    lookup_field='id'

    def get_queryset(self):
        return Course.objects.select_related('author',"category").filter(
            category__id=self.kwargs[self.lookup_field]
        ).all()


# apps views
class CreateReviewApiView(CreateAPIView):
    serializer_class=ReviewSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    lookup_field='id'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reviewed_course=get_object_or_404(Course,id=self.kwargs[self.lookup_field])
        data=serializer.save(user=self.request.user,course=reviewed_course)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# apps views
class ReviewApiView(ListAPIView):
    serializer_class=ReviewSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]
    lookup_field='id'

    def get_queryset(self):
        return Review.objects.select_related('course','user').\
            filter(course__id=self.kwargs[self.lookup_field]).all()

# apps views
class SubCourseApiView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]
    lookup_field='id'

    def get(self, request, *args, **kwargs):
        try:
            obj=SubCourse.objects.select_related('course',).\
                prefetch_related('subcourse_lesson').filter(course=self.kwargs[self.lookup_field])
            self.check_object_permissions(self.request, obj)
            if self.request.user.enroll_courses\
                .prefetch_related("course__author__enroll_courses").filter(id__in=[self.kwargs[self.lookup_field]]).exists():
                serializer=EnrollSubCourseOutputSerializer(obj,many=True,context={"request":self.request})
            else:
               serializer=SubCourseOutputSerializer(obj,many=True,context={"request":self.request})
        except Exception as e:
            data={
                "message":error_handler(e),
                "status":"failed"     
            }
            raise NotFound(data)
        return Response(serializer.data)
    

