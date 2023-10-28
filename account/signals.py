# from django.core.mail import EmailMultiAlternatives
# from django.conf import settings
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from django.template.loader import render_to_string
# from django.utils.encoding import smart_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.urls import reverse

# # smart_bytes convert your uid to byte and urlsafe_base64 convert to save string


# @receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="unique_identifier")
# def send_confirmation_email(sender, instance, created, **kwargs):
#     if created:
#         try:
#             subject = 'Confirm Your Email Address'
#             message = render_to_string('accounts/email_confirmation.html', {
#             'user': instance,
#             'domain': settings.DOMIN,
#             'protocol':settings.PROTOCOL,
#             'uid': urlsafe_base64_encode(smart_bytes(instance.pk)),
#             'token': default_token_generator.make_token(instance),
#         }) 
#             from_email = settings.EMAIL_HOST_USER
#             to_email = instance.email
#             # send_mail(subject, message, from_email, [to_email], fail_silently=False)
#             msg = EmailMultiAlternatives(subject, message, from_email, [to_email])
#             msg.attach_alternative(message, "text/html")
#             msg.send()
#         except Exception as e:
#             print(f'Error sending confirmation email: {e}')
