from rest_framework.generics import CreateAPIView
from .serializers import MyLearningSerializer,EnrolledCourseOutputSerializer,OngoingCourseDetailSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.error_handler import error_handler
from courses.models import Lesson
from rest_framework import status
from django.db import transaction
from rest_framework.exceptions import NotFound,ValidationError
from .services import enroll_to_course
from django.db.models import Avg,Sum,Count,Q,When,Case,F
from courses.models import Course,SubCourse
from django.shortcuts import get_object_or_404
# Create your views here.
class MyLearningApiView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]
    
    def get(self, request, *args, **kwargs):
        try:
            obj=self.request.user.enroll_courses\
                .select_related("author").prefetch_related("lessons")\
                    .annotate(total_lesson=Count('lessons'),
                              completed_lesson=Count('lessons__is_completed',filter=Q(lessons__is_completed=self.request.user)),
                                                     complete_course=Case(When(total_lesson=F("completed_lesson"),then=True),
                                 default=False))\
                                 .exclude(complete_course=True).all()
            
            self.check_object_permissions(self.request, obj)
            serializer = EnrolledCourseOutputSerializer(obj,many=True,context={'request':self.request})
        except Exception as e:
            raise ValidationError(error_handler(e))
        return Response(serializer.data)
    

class EnrollApiView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            data=enroll_to_course(course_id=self.kwargs['id'],user=self.request.user)
        except Exception as e:
            raise ValidationError(error_handler(e))
        return Response(data)



class AutoAddLessonCompleteApiView(CreateAPIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    lookup_field='id'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            get_lesson=Lesson.objects.get(id=self.kwargs[self.lookup_field])
            if get_lesson.is_completed.filter(id=self.request.user.id).exists():
                get_lesson.is_completed.remove(self.request.user)
                context={
                    'message':"not completed",
                    "status":False
                }
            else:
                get_lesson.is_completed.add(self.request.user)
                context={
                    'message':"completed",
                    "status":True
                }
        except Exception as e:
            raise NotFound(error_handler(e))
        return Response(context, status=status.HTTP_201_CREATED)



class CompletedCourse(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]
    
    def get(self, request, *args, **kwargs):
        try:
            obj=self.request.user.enroll_courses\
                .select_related("author").prefetch_related("lessons")\
                    .annotate(total_lesson=Count('lessons'),
                              completed_lesson=Count('lessons__is_completed',filter=Q(lessons__is_completed=self.request.user)),
                                                     complete_course=Case(When(total_lesson=F("completed_lesson"),then=True),
                                 default=False))\
                                 .exclude(complete_course=False).all()
            self.check_object_permissions(self.request, obj)
            serializer = EnrolledCourseOutputSerializer(obj,many=True,context={'request':self.request})
        except Exception as e:
            raise ValidationError(error_handler(e))
        return Response(serializer.data)
    

class OnGoingDetail(ListAPIView):
    serializer_class=OngoingCourseDetailSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]
    lookup_field='id'
    

    def get_queryset(self):
        return SubCourse.objects.filter(course=self.kwargs['id']).annotate(complete_video=Case(
            When(Q(subcourse_lesson__is_completed=self.request.user),then=True),
            default=False
        )).prefetch_related("subcourse_lesson").all()