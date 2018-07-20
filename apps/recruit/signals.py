import logging
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from recruit.models import Company


User = get_user_model()
logger = logging.getLogger('recruit')


@receiver(post_save, sender=Company)
def company_create(sender, instance=None, created=False, **kwargs):
    if created:
        # 新企业提交认证 通知业务人员进行审核
        logging.info('新企业认证-企业名称:{};联系人姓名:{};联系人电话:{}'.format(instance.name, instance.user.nickname, instance.user.mobile))


@receiver(post_save, sender=Company)
def recruit_order_can_show_by_company(sender, instance=None, created=False, **kwargs):
    # 企业通过审核通过, 招募令解禁
    if instance.status == 30:
        logging.info('企业通过审核通过, 招募令解禁')

