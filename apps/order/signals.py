import copy
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from .models import OrderInfo
from .tasks import order_deposit_pay_refund_monitor
from accounts.models import BalanceDetail
from .tasks import order_create_send_email_notice


User = get_user_model()


@receiver(post_init, sender=OrderInfo)
def order_complete_init(instance=None, **kwargs):
    instance.__original_status = instance.status

@receiver(post_save, sender=OrderInfo)
def order_complete(sender, instance=None, created=False, **kwargs):
    if instance.__original_status != instance.status and instance.status == 11:
        messgae = '{}有新订单({})啦, 内容"{}" ；请尽快处理'.format(instance.school.name, instance.id, instance.description)
        email_list = copy.deepcopy(settings.EMAIL_ORDER_CREATE_NOTICE)
        user_list = User.objects.filter(profileextendinfo__admin_school=instance.school)
        for user in user_list:
            if user.email:
                email_list.append(user.email)
        order_create_send_email_notice.apply_async(args=(messgae, email_list,), )
    if instance.__original_status != instance.status and instance.status == 50:
        # todo 监听订单状态为50后的
        # 1.佣兵账户余额增加
        if BalanceDetail.objects.filter(user=instance.receiver_user, origin_type='10', order=instance.id).count():
            return
        BalanceDetail.objects.create(
            user=instance.receiver_user,
            origin_type='10',
            order=instance.id,
            balance=instance.reward
        )
        #  2.押金退回
        order_deposit_pay_refund_monitor.apply_async(args=(instance.id,), )
