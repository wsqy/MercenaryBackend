from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderInfo
from .tasks import order_deposit_pay_refund_monitor
from accounts.models import BalanceDetail
from .tasks import order_create_send_email_notice


@receiver(post_save, sender=OrderInfo)
def order_complete(sender, instance=None, created=False, **kwargs):
    if instance.status == 11:
        order_create_send_email_notice.apply_async(args=('测试邮件到达:订单号--{}'.format(instance.id),))
    if instance.status == 50:
        # todo 监听订单状态为50后的
        # 1.佣兵账户余额增加
        BalanceDetail.objects.create(
            user=instance.receiver_user,
            origin_type='10',
            order=instance.id,
            balance=instance.reward
        )
        #  2.押金退回
        order_deposit_pay_refund_monitor.apply_async(args=(instance.id,), )
