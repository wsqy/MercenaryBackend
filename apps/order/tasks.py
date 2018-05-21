from django.db.models import Q
from datetime import datetime, timedelta
from celery import task

from .models import OrderInfo
from paycenter.models import PayOrder
from utils.pay import alipay


@task(bind=True)
def order_reward_pay_timeout_monitor(self, order_id):
    # 佣金支付超时监控
    order_list = OrderInfo.objects.filter(id=order_id)
    for order in order_list:
        if order.status in (1, 2):
            order.status = -21
            order.save()


@task(bind=True)
def order_deposit_pay_timeout_monitor(self, order_id):
    # 押金支付超时监控
    order_list = OrderInfo.objects.filter(id=order_id)
    for order in order_list:
        if order.status in (12, 13):
            order.status = 11
            order.receiver_user = None
            order.receiver_confirm_time = None
            order.save()


@task(bind=True)
def order_reward_pay_refund_monitor(self, order_id, status=-23):
    # 佣金/赏金退款接口
    try:
        order = OrderInfo.objects.get(id=order_id)
    except Exception as e:
        return

    reward_pay_order_list = PayOrder.objects.filter(order=order, status=3)
    reward_pay_order_list = reward_pay_order_list.filter(Q(order_type=3) | Q(order_type=2))
    # print("支付订单总数:{}".format(reward_pay_order_list.count()))
    for reward_pay_order in reward_pay_order_list:
        # print('待退款{}--支付方式{}'.format(reward_pay_order.id, reward_pay_order.pay_method))
        if reward_pay_order.pay_method == 1:
            r_dict = alipay.refund_request(
                out_trade_no=reward_pay_order.id,
                refund_amount=reward_pay_order.pay_cost / 100,
                refund_reason='订单超时未接, 全额退款'
            )
            try:
                if r_dict.get('alipay_trade_refund_response', {}).get('code') != '10000':
                    raise Exception('alipay order: {} reward refound error'.format(order_id))
            except Exception as e:
                print("退款异常")
                raise self.retry(exc=e, eta=datetime.utcnow() + timedelta(seconds=60), max_retries=5)
    order.status = status
    order.save()


@task(bind=True)
def order_deposit_pay_refund_monitor(self, order_id):
    # 押金退款接口
    try:
        order = OrderInfo.objects.get(id=order_id)
    except Exception as e:
        return
    # 正常退押金 状态必为20+
    if order.status <= 20:
        return

    reward_pay_order_list = PayOrder.objects.filter(order=order, order_type=1, status=3)
    for reward_pay_order in reward_pay_order_list:
        if reward_pay_order.pay_method == 1:
            r_dict = alipay.refund_request(
                out_trade_no=reward_pay_order.id,
                refund_amount=reward_pay_order.pay_cost / 100,
                refund_reason='订单已完成, 退还押金'
            )

            try:
                if r_dict.get('code') != '10000':
                    raise Exception('alipay order: {} deposit refound error'.format(order_id))
            except Exception as e:
                raise self.retry(exc=e, eta=datetime.utcnow() + timedelta(seconds=60), max_retries=5)


@task(bind=True)
def order_complete_monitor(self, order_id):
    # 佣兵点击完成后
    order_list = OrderInfo.objects.filter(id=order_id, status=21)
    for order in order_list:
        order.status = 50
        order.save()
