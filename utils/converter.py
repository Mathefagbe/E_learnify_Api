from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode


@staticmethod
def bytes_Converter(uid):
    decode_uid=urlsafe_base64_decode(uid)
    uid_to_string=smart_str(decode_uid)
    return uid_to_string


