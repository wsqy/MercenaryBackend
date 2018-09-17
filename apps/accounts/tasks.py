import logging

from celery import task
from django.core.mail import send_mail
from django.conf import settings


logger = logging.getLogger('recruit')


@task(bind=True)
def with_draw_send_email_notice(self, to_email):
    subject = '提现申请'
    message = '有新的提现申请啦" ；请尽快处理'
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        result = send_mail(subject, message, from_email, to_email, fail_silently=False)
        logging.info('邮件发送结果: {}-{}--结果{}'.format(from_email, to_email, result))
    except Exception as e:
        logging.error('邮件发送失败: {}-{}--结果{}--异常原因{}'.format(from_email, to_email, result, e))