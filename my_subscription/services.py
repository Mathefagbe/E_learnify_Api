from courses.models import Course
from rest_framework.exceptions import NotFound
from utils.error_handler import error_handler


@staticmethod
def enroll_to_course(course_id,user):
        try:
            get_course=Course.objects.get(id=course_id)
            get_course.subscribers.add(user)
            context={
                'status':f'congratulations You Have successfully Enrolled For {get_course.title}'
            }
        except Exception as e:
            raise NotFound(error_handler(e))
        return context