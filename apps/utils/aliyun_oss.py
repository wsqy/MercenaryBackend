import oss2

from django.conf import settings
from django.utils import timezone


class Oss:
    def __init__(self):
        self.__ACCESS_KEY_ID = settings.ACCESS_KEY_ID
        self.__ACCESS_KEY_SECRET = settings.ACCESS_KEY_SECRET
        self.__END_POINT = settings.END_POINT
        self.__BUCKET_NAME = settings.BUCKET_NAME
        self.__oss_auth = oss2.Auth(self.__ACCESS_KEY_ID, self.__ACCESS_KEY_SECRET)
        self.__bucket = oss2.Bucket(self.__oss_auth, self.__END_POINT, self.__BUCKET_NAME)

    def user_upload_portrait(self, file_obj, oss_file):
        self.__bucket.put_object('{}/{}'.format(timezone.now().strftime("%Y%m%d"), oss_file), file_obj)
