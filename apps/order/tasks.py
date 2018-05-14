from .models import OrderInfo
from celery import shared_task


@shared_task
def order_reward_pay_timeout_monitor(order_id):
    # 佣金支付超时监控
    order_list = OrderInfo.objects.filter(id=order_id)
    for order in order_list:
        if order.status in (1, 2):
            order.status = -21
            order.save()


@shared_task
def order_deposit_pay_timeout_monitor(order_id):
    # 押金支付超时监控
    order_list = OrderInfo.objects.filter(id=order_id)
    for order in order_list:
        if order.status in (12, 13):
            order.status = -22
            order.receiver_user = None
            order.receiver_confirm_time = None
            order.save()
