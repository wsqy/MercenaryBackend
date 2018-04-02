import oss2
import time, random
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

    def user_upload_portrait(self, file_obj):
        mulu = timezone.now().strftime('%Y%m%d')
        oss_filename = '{}/{}{}.png'.format(mulu, int(time.time() * 100000000), random.randrange(1000, 9999))
        self.__bucket.put_object(oss_filename, file_obj)
        return oss_filename
