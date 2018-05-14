import oss2
from django.conf import settings


class Oss:
    def __init__(self):
        self.__ACCESS_KEY_ID = settings.OSS_ACCESS_KEY_ID
        self.__ACCESS_KEY_SECRET = settings.OSS_ACCESS_KEY_SECRET
        self.__END_POINT = settings.END_POINT
        self.__BUCKET_NAME = settings.BUCKET_NAME
        self.__oss_auth = oss2.Auth(self.__ACCESS_KEY_ID, self.__ACCESS_KEY_SECRET)
        self.__bucket = oss2.Bucket(self.__oss_auth, self.__END_POINT, self.__BUCKET_NAME)

    def user_upload_portrait(self, file_obj, oss_filename):
        self.__bucket.put_object(oss_filename, file_obj)
        return 'https://{}.{}/{}'.format(settings.BUCKET_NAME, settings.END_POINT, oss_filename)
