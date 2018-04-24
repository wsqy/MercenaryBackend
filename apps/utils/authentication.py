from django.conf import settings
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


def CommonAuthentication():
    authentication_classes = [JSONWebTokenAuthentication]
    if settings.DEBUG:
        authentication_classes.append(authentication.SessionAuthentication)
    return authentication_classes