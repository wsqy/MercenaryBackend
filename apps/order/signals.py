from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderInfo
from .tasks import order_deposit_pay_refund_monitor


@receiver(post_save, sender=OrderInfo)
def order_complete(sender, instance=None, created=False, **kwargs):
    if instance.status == 50:
        # todo 监听订单状态为50后的 1.佣兵账户余额增加;2.押金退回
        order_deposit_pay_refund_monitor.apply_async(args=(instance.id,), )
