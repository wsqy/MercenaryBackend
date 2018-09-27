import logging
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_init

from recruit.models import Company, PartTimeOrder
from .tasks import recruit_cancel


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


@receiver(post_init, sender=PartTimeOrder)
def recruit_order_cancel_init(instance=None, **kwargs):
    instance.__original_status = instance.status


@receiver(post_save, sender=PartTimeOrder)
def recruit_order_cancel_save(sender, instance=None, created=False, **kwargs):
    if not created and instance.__original_status != instance.status and instance.status == -20:
        logging.info('商户取消兼职招募令')
        recruit_cancel.apply_async(args=(instance.id, '商户取消兼职招募令退款'))
