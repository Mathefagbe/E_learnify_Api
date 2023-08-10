from rest_framework.generics import CreateAPIView
from .serializers import MyLearningSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.error_handler import error_handler
from courses.models import Lesson
from rest_framework import status
from django.db import transaction
from rest_framework.exceptions import NotFound,ValidationError


# Create your views here.
class MyLearningApiView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]
    
    def get(self, request, *args, **kwargs):
        try:
            obj=self.request.user
            self.check_object_permissions(self.request, obj)
            serializer = MyLearningSerializer(obj,many=False,context={'user':self.request.user})
        except Exception as e:
            raise ValidationError(error_handler(e))
        return Response(serializer.data)



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
                    'status':"not completed"
                }
            else:
                get_lesson.is_completed.add(self.request.user)
                context={
                    'status':"completed"
                }
        except Exception as e:
            raise NotFound(error_handler(e))
        return Response(context, status=status.HTTP_201_CREATED)



