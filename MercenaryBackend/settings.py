"""
Django settings for MercenaryBackend project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys

from django.utils import timezone

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wiih3k9w*b!3gmu05g8s*387l5&z@*!ie5idka9w%)jn#!5o+%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'users.ProfileInfo'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'xadmin',
    'crispy_forms',
    'django_filters',
    'rest_framework',
    'django_celery_results',
    'aliyun_oss2_storage',
    'raven.contrib.django.raven_compat',
    'users.apps.UsersConfig',
    'area.apps.AreaConfig',
    'order.apps.OrderConfig',
    'paycenter.apps.PaycenterConfig',
    'accounts.apps.AccountsConfig',
    'resources.apps.ResourcesConfig',
    'recruit.apps.RecruitConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MercenaryBackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MercenaryBackend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "eros",
        'USER': 'eros',
        'PASSWORD': "tRFy7z8ht",
        'HOST': "127.0.0.1",
        'OPTIONS': {
            'autocommit': True,
            'init_command': 'SET default_storage_engine=INNODB',
            'charset': 'utf8mb4',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
# 中文支持
LANGUAGE_CODE = 'zh-hans'
# 设置时区
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True
# 默认是Ture，时间是utc时间，由于我们要用本地时间，所用手动修改为false！！！！
USE_TZ = False

# 验证码过期时间
VERIFY_CODE_EXPIRE_TIME = 5 * 60
VERIFY_CODE_EXPIRE_TIME_DEFAULT = 5 * 60

# 注册短信有效期
REGEISTER_SMS_EXPIRE_TIME_DEFAULT = '5分钟'

# 验证后端
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)

# drf配置
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
#     ),
# }

# jwt配置
JWT_AUTH = {
    # token过期时间
    'JWT_EXPIRATION_DELTA': timezone.timedelta(days=1),
    'JWT_ALLOW_REFRESH': True,
}

# 阿里大于短信配置
SMS_ACCESS_KEY_ID = 'LTAISSYn8u9H4Q4u'
SMS_ACCESS_KEY_SECRET = 'rXFZmpAFgmiIUGxtaPW9Ron0nd8YQ4'

# 验证码类别
REGISTER_CODE_TYPE = 'SMS_76310006'
FORGET_PASSWD_CODE_TYPE = 'SMS_76270012'
CODE_TYPE = {
    REGISTER_CODE_TYPE: '注册验证码',
    FORGET_PASSWD_CODE_TYPE: '找回密码验证码',
}

# 阿里云oss相关配置
ACCESS_KEY_ID = 'LTAIgl1IpdAdgnJX'
ACCESS_KEY_SECRET = 'm5ohdxa6L04acDrYmauLRKbs69CTOC'
END_POINT = 'oss-cn-shenzhen.aliyuncs.com'
ALIYUN_OSS_CNAME = ''
BUCKET_NAME = 'mercenary-user-up'
BUCKET_ACL_TYPE = 'public-read'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# mediafile将自动上传
DEFAULT_FILE_STORAGE = 'aliyun_oss2_storage.backends.AliyunMediaStorage'

REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_CELERY_BROKER_URL = '1'
REDIS_RESULT_BACKEND = '1'
REDIS_PASSWD = 'f886Yjhvuyfy76grhgdFYrtf'
REDIS_CONN_NOPASSWD = "redis://%s:%s/%s"
REDIS_CONN_WITHPASS = "redis://:%s@%s:%s/%s"

CELERY_BROKER_URL = REDIS_CONN_WITHPASS % (REDIS_PASSWD, REDIS_HOST, REDIS_PORT, REDIS_CELERY_BROKER_URL)
CELERY_RESULT_BACKEND = REDIS_CONN_WITHPASS % (REDIS_PASSWD, REDIS_HOST, REDIS_PORT, REDIS_RESULT_BACKEND)
CELERY_ENABLE_UTC = False  # 不用UTC.
CELERY_TIMEZONE = 'Asia/Shanghai'   # 指定上海时区

# 日志配置
LOGGING = {
    'version': 1,
    # 使用True代表 默认配置中的所有logger 都将禁用，小心使用  一般都是Flase
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        # 正常只使用下面这种
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s %(message)s]'
        },
    },
    'filters': {
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join("log", 'all.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join("log", 'error.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join("log", 'script.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'scprits_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join("log", 'script.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'scripts': {
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False,
        },
        'users': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'order': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'paycenter': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'accounts': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': True,
        },

    }
}

# 项目的基本配置
# 手续费(百分制)
SERVICE_COST = 15

# 订单付款超时时间
PAY_DEFAULT_EXPIRE_TIME = 30 * 60
# 押金支付超时时间
PAY_DEPOSIT_EXPIRE_TIME = 5 * 60
# 佣兵点击完成到订单完成的时间间隔
PAY_COMPLETE_EXPIRE_TIME = 2 * 60 * 60
#####  支付相关  #####
PAY_KEY_BASE_URL = os.path.join(BASE_DIR, 'apps/utils/keys')
ALIPAY_APPID = '2017080508049336'
ALIPAY_NOTIFY_URL = 'http://118.24.157.119:8000/pay/return/alipay/'
ALIPAY_PRIVATE_KEY_PATH = os.path.join(PAY_KEY_BASE_URL, 'private_2048.txt')
ALIPAY_ALI_PUBLIC_KEY_PATH = os.path.join(PAY_KEY_BASE_URL, 'alipay_public_2048.txt')
ALIPAY_RETURN_URL = 'http://118.24.157.119:8000/pay/return/alipay/'
ALIPAT_EXPIRE_TIME = 30 * 60

WXPAY_APP_APPID = 'wx11246b0732973381'
WXPAY_APP_MCH_ID = '1486240842'
WXPAY_APP_KEY = 'm12MGa0wQvD8XdArznO9hecRxWiPpobK'
WXPAY_APP_CERT_PEM_PATH = os.path.join(PAY_KEY_BASE_URL, 'apiclient_cert.pem')
WXPAY_APP_KEY_PEM_PATH = os.path.join(PAY_KEY_BASE_URL, 'apiclient_key.pem')
WXPAY_APP_NOTIFY_URL = 'http://118.24.157.119:8000/pay/return/wxpay/'
#####  支付相关  #####

# 银行英文简称全称对照
BANK_CARD = {
  'SRCB': '深圳农村商业银行',
  'BGB': '广西北部湾银行',
  'SHRCB': '上海农村商业银行',
  'BJBANK': '北京银行',
  'WHCCB': '威海市商业银行',
  'BOZK': '周口银行',
  'KORLABANK': '库尔勒市商业银行',
  'SPABANK': '平安银行',
  'SDEB': '顺德农商银行',
  'HURCB': '湖北省农村信用社',
  'WRCB': '无锡农村商业银行',
  'BOCY': '朝阳银行',
  'CZBANK': '浙商银行',
  'HDBANK': '邯郸银行',
  'BOC': '中国银行',
  'BOD': '东莞银行',
  'CCB': '中国建设银行',
  'ZYCBANK': '遵义市商业银行',
  'SXCB': '绍兴银行',
  'GZRCU': '贵州省农村信用社',
  'ZJKCCB': '张家口市商业银行',
  'BOJZ': '锦州银行',
  'BOP': '平顶山银行',
  'HKB': '汉口银行',
  'SPDB': '上海浦东发展银行',
  'NXRCU': '宁夏黄河农村商业银行',
  'NYNB': '广东南粤银行',
  'GRCB': '广州农商银行',
  'BOSZ': '苏州银行',
  'HZCB': '杭州银行',
  'HSBK': '衡水银行',
  'HBC': '湖北银行',
  'JXBANK': '嘉兴银行',
  'HRXJB': '华融湘江银行',
  'BODD': '丹东银行',
  'AYCB': '安阳银行',
  'EGBANK': '恒丰银行',
  'CDB': '国家开发银行',
  'TCRCB': '江苏太仓农村商业银行',
  'NJCB': '南京银行',
  'ZZBANK': '郑州银行',
  'DYCB': '德阳商业银行',
  'YBCCB': '宜宾市商业银行',
  'SCRCU': '四川省农村信用',
  'KLB': '昆仑银行',
  'LSBANK': '莱商银行',
  'YDRCB': '尧都农商行',
  'CCQTGB': '重庆三峡银行',
  'FDB': '富滇银行',
  'JSRCU': '江苏省农村信用联合社',
  'JNBANK': '济宁银行',
  'CMB': '招商银行',
  'JINCHB': '晋城银行JCBANK',
  'FXCB': '阜新银行',
  'WHRCB': '武汉农村商业银行',
  'HBYCBANK': '湖北银行宜昌分行',
  'TZCB': '台州银行',
  'TACCB': '泰安市商业银行',
  'XCYH': '许昌银行',
  'CEB': '中国光大银行',
  'NXBANK': '宁夏银行',
  'HSBANK': '徽商银行',
  'JJBANK': '九江银行',
  'NHQS': '农信银清算中心',
  'MTBANK': '浙江民泰商业银行',
  'LANGFB': '廊坊银行',
  'ASCB': '鞍山银行',
  'KSRB': '昆山农村商业银行',
  'YXCCB': '玉溪市商业银行',
  'DLB': '大连银行',
  'DRCBCL': '东莞农村商业银行',
  'GCB': '广州银行',
  'NBBANK': '宁波银行',
  'BOYK': '营口银行',
  'SXRCCU': '陕西信合',
  'GLBANK': '桂林银行',
  'BOQH': '青海银行',
  'CDRCB': '成都农商银行',
  'QDCCB': '青岛银行',
  'HKBEA': '东亚银行',
  'HBHSBANK': '湖北银行黄石分行',
  'WZCB': '温州银行',
  'TRCB': '天津农商银行',
  'QLBANK': '齐鲁银行',
  'GDRCC': '广东省农村信用社联合社',
  'ZJTLCB': '浙江泰隆商业银行',
  'GZB': '赣州银行',
  'GYCB': '贵阳市商业银行',
  'CQBANK': '重庆银行',
  'DAQINGB': '龙江银行',
  'CGNB': '南充市商业银行',
  'SCCB': '三门峡银行',
  'CSRCB': '常熟农村商业银行',
  'SHBANK': '上海银行',
  'JLBANK': '吉林银行',
  'CZRCB': '常州农村信用联社',
  'BANKWF': '潍坊银行',
  'ZRCBANK': '张家港农村商业银行',
  'FJHXBC': '福建海峡银行',
  'ZJNX': '浙江省农村信用社联合社',
  'LZYH': '兰州银行',
  'JSB': '晋商银行',
  'BOHAIB': '渤海银行',
  'CZCB': '浙江稠州商业银行',
  'YQCCB': '阳泉银行',
  'SJBANK': '盛京银行',
  'XABANK': '西安银行',
  'BSB': '包商银行',
  'JSBANK': '江苏银行',
  'FSCB': '抚顺银行',
  'HNRCU': '河南省农村信用',
  'COMM': '交通银行',
  'XTB': '邢台银行',
  'CITIC': '中信银行',
  'HXBANK': '华夏银行',
  'HNRCC': '湖南省农村信用社',
  'DYCCB': '东营市商业银行',
  'ORBANK': '鄂尔多斯银行',
  'BJRCB': '北京农村商业银行',
  'XYBANK': '信阳银行',
  'ZGCCB': '自贡市商业银行',
  'CDCB': '成都银行',
  'HANABANK': '韩亚银行',
  'CMBC': '中国民生银行',
  'LYBANK': '洛阳银行',
  'GDB': '广东发展银行',
  'ZBCB': '齐商银行',
  'CBKF': '开封市商业银行',
  'H3CB': '内蒙古银行',
  'CIB': '兴业银行',
  'CRCBANK': '重庆农村商业银行',
  'SZSBK': '石嘴山银行',
  'DZBANK': '德州银行',
  'SRBANK': '上饶银行',
  'LSCCB': '乐山市商业银行',
  'JXRCU': '江西省农村信用',
  'ICBC': '中国工商银行',
  'JZBANK': '晋中市商业银行',
  'HZCCB': '湖州市商业银行',
  'NHB': '南海农村信用联社',
  'XXBANK': '新乡银行',
  'JRCB': '江苏江阴农村商业银行',
  'YNRCC': '云南省农村信用社',
  'ABC': '中国农业银行',
  'GXRCU': '广西省农村信用',
  'PSBC': '中国邮政储蓄银行',
  'BZMD': '驻马店银行',
  'ARCU': '安徽省农村信用社',
  'GSRCU': '甘肃省农村信用',
  'LYCB': '辽阳市商业银行',
  'JLRCU': '吉林农信',
  'URMQCCB': '乌鲁木齐市商业银行',
  'XLBANK': '中山小榄村镇银行',
  'CSCB': '长沙银行',
  'JHBANK': '金华银行',
  'BHB': '河北银行',
  'NBYZ': '鄞州银行',
  'LSBC': '临商银行',
  'BOCD': '承德银行',
  'SDRCU': '山东农信',
  'NCB': '南昌银行',
  'TCCB': '天津银行',
  'WJRCB': '吴江农商银行',
  'CBBQS': '城市商业银行资金清算中心',
  'HBRCU': '河北省农村信用社'
}
# 银行卡类型对照
BANK_CARD_TYPE = {
    'DC': '储蓄卡',
    'CC': '信用卡',
    'SCC': '贷记卡',
    'DCC': '存贷合一卡',
    'PC': '预付卡',
    'STPB': '标准存折',
    'STFA': '标准对公账户',
    'NSTFA': '非标准对公账户',
}

# 支付宝
ALIPAY_MARKET_AUTH_APPCODE = '37364b8dd8634447ba623db5a4782ea5'


# 发送邮件配置(腾讯企业邮)
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_HOST_USER = 'open@mercenary.com.cn'
EMAIL_HOST_PASSWORD = '90Hju88y'
# 腾讯云 465 端口发送邮件没有测试成功  如果在新得服务器上测试成功 可以使用465 端口
# EMAIL_PORT = 465
# EMAIL_USE_TLS = True
EMAIL_PORT = 25
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


RAVEN_CONFIG = {
    'dsn': 'https://149493d6ba7f466fa8dbb5359490d737:09e8d58195324c79903882741fb426f3@sentry.io/1219835',
}

try:
    from .local_settings import *
except:
    pass
