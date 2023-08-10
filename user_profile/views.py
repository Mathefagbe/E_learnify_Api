from django.shortcuts import render,get_object_or_404
from rest_framework.generics import RetrieveAPIView,CreateAPIView
from .serializers import InstructorSerializer,UserSerializer
from .models import Profile
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class InstructorProfileApiView(RetrieveAPIView):
    serializer_class=InstructorSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    lookup_field="id"

    def get_queryset(self):
        return Profile.objects.select_related('user').all()
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        obj = get_object_or_404(queryset, user__id=self.kwargs[lookup_url_kwarg])
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj
    

class UserProfileApiView(RetrieveAPIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
  
    def get_queryset(self):
        return Profile.objects.select_related('user').all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, user__id=self.request.user.id)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return InstructorSerializer
        return UserSerializer
    
class UserProfileCreateApiView(CreateAPIView):
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
  
    def get_queryset(self):
        return Profile.objects.select_related('user').all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, user__id=self.request.user.id)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj
    
    # def get_serializer_class(self):
    #     if self.request.user.is_staff:
    #         return InstructorSerializer
    #     return UserSerializer