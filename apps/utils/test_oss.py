import oss2

ACCESS_KEY_ID = 'LTAIgl1IpdAdgnJX'
ACCESS_KEY_SECRET = 'm5ohdxa6L04acDrYmauLRKbs69CTOC'
END_POINT = 'oss-cn-shenzhen.aliyuncs.com'
BUCKET_NAME = 'mercenary-user-up'
BUCKET_ACL_TYPE = 'public-read'

oss_auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(oss_auth, END_POINT, BUCKET_NAME)


def test_upload(filename):
    with open(oss2.to_unicode(filename), 'wb') as f:
        return bucket.put_object(filename, f)


res = test_upload('test01.png')
