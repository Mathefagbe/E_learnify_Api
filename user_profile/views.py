from django.shortcuts import render,get_object_or_404
from rest_framework.generics import RetrieveAPIView,RetrieveUpdateAPIView
from .serializers import InstructorSerializer,UserSerializer
from .models import UserProfile,InstructorProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import FormParser,MultiPartParser,JSONParser

# Create your views here.
class InstructorProfileApiView(RetrieveAPIView):
    serializer_class=InstructorSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    lookup_field="id"

    def get_queryset(self):
        return InstructorProfile.objects.select_related('instructor').all()
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        obj = get_object_or_404(queryset, user__id=self.kwargs[lookup_url_kwarg])
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj
    

class UserProfileApiView(RetrieveUpdateAPIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    serializer_class=UserSerializer
    http_method_names=['get','patch']
    parser_classes=[MultiPartParser,FormParser,JSONParser]

    def get_queryset(self):
        return UserProfile.objects.select_related('user').all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, user__id=self.request.user.id)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj

    






# from .models import Profile
# from requests import request,HTTPError
# from django.core.files.base import ContentFile
# def save_social_profile(strategy,deatils,backend,user,response,is_new=False,*args,**kwargs):
#     if is_new and backend.name=='facebook':
#         Profile.objects.filter(user=user).update(
#             imageurl='https://graph.facebook.com/{0}/picture/?type=large&access_token={1}'.format(
#             response['id'],response['access_token']
#             )
#         )

#         Profile.objects.filter(user=user).update(
#             imageurl='https://graph.facebook.com/{0}/picture/?type=large&access_token={1}'.format(
#             response['id'],response['access_token']
#             )
#         )
#         url='http://graph.facebook.com/{0}/picture'.format(response['id'])
#         try:
#             response=request('GET',url,params={
#                 'type':'large'
#             })
#             response.raise_for_status()
#         except HTTPError:
#             pass
#         else:
#             pass
#             # profile=user.get_profile
#             # profile.profile_phote.save(f"{user.name},social.jpg",ContentFile(response.content))
#             # profile.save
