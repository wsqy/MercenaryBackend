import json

from celery import shared_task
from utils.dayu import DaYuSMS


@shared_task
def dayu_send_sms(phone, type, params):
    try:
        res = DaYuSMS().send_sms(phone_numbers=phone, template_code=type, template_param=params)
        res = json.loads(bytes.decode(res))
    except Exception as e:
        res = {'Code': 'UNKNOWN_ERROR'}
    return res
