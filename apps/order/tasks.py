import logging
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from celery import task
from django.core.mail import send_mail
from django.conf import settings

from .models import OrderInfo, OrderOperateLog
from paycenter.models import PayOrder
from utils.pay import alipay, wxpay
from utils.common import generate_random_number

logger = logging.getLogger('order')

@task(bind=True)
def order_reward_pay_timeout_monitor(self, order_id):
    # 佣金支付超时监控
    order_list = OrderInfo.objects.filter(id=order_id)
    for order in order_list:
        if order.status in (1, 2):
            order.status = -21
            order.save()
            OrderOperateLog.logging(order=order, message='佣金支付超时')


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
            OrderOperateLog.logging(order=order, message='押金支付超时')


def paycenter_refund(reward_pay_order_list, refund_mes='订单退款'):
    """
    :param reward_pay_order_list: 待退款订单列表
    :return: 退款是否成功
    """
    logger.info('支付订单总数:{}'.format(reward_pay_order_list.count()))
    for reward_pay_order in reward_pay_order_list:
        logger.info('待退款{}--支付方式{}--类型{}'.format(reward_pay_order.id, reward_pay_order.pay_method, reward_pay_order.order_type))
        if reward_pay_order.pay_method == 1:
            logger.info('alipay订单退款')
            r_dict = alipay.refund_request(
                out_trade_no=reward_pay_order.id,
                refund_amount=reward_pay_order.pay_cost / 100,
                refund_reason=refund_mes
            )
            alipay_response = r_dict.get('alipay_trade_refund_response', {})
            logger.info('alipay订单状态{}'.format(alipay_response))
            if alipay_response.get('code') != '10000':
                 return False
        elif reward_pay_order.pay_method == 2:
            logger.info('wxpay订单退款')
            r_dict = wxpay.refund_request(
                out_trade_no=reward_pay_order.id,
                out_refund_no='{}{}'.format(reward_pay_order.id, generate_random_number(4)),
                total_fee=reward_pay_order.pay_cost,
                refund_fee=reward_pay_order.pay_cost,
                refund_desc=refund_mes
            )
            logger.info('wxpay订单状态{}'.format(r_dict))
            if not wxpay.is_pay_success(r_dict):
                return False
        reward_pay_order.status = 4
        reward_pay_order.save()
    return True


@task(bind=True)
def order_reward_pay_refund_monitor(self, order_id, status=-23):
    # 佣金/赏金退款接口
    logger.info('佣金/赏金退款接口--{}, 待变更状态--{}'.format(order_id, status))
    try:
        order = OrderInfo.objects.get(id=order_id)
    except Exception as e:
        logger.error('佣金/赏金退款接口, 获取订单异常--{}'.format(e))
        return

    reward_pay_order_list = PayOrder.objects.filter(order=order, status=3)
    reward_pay_order_list = reward_pay_order_list.filter(Q(order_type=3) | Q(order_type=2))
    logger.info('支付订单总数in line:{}'.format(reward_pay_order_list.count()))
    refund_mes = '订单超时未接, 全额退款'
    if status == -23:
        if order.status not in (1, 2, 11):
            logger.info('订单:{}-不符合超时取消条件'.format(order_id))
            return
        refund_mes = '订单超时未接, 全额退款'
    elif status == -12:
        refund_mes = '雇主主动取消, 全额退款'
    elif status == -15:
        refund_mes = '客服操作取消, 全额退款'
    refund_status = paycenter_refund(reward_pay_order_list, refund_mes=refund_mes)
    try:
        assert refund_status
        OrderOperateLog.logging(order=order, message=refund_mes)
    except Exception as e:
        logging.error('佣金/赏金退款失败, 再次发起退款')
        raise self.retry(exc=e, countdown=60, max_retries=5)

    order.status = status
    order.save()


@task(bind=True)
def order_deposit_pay_refund_monitor(self, order_id):
    # 押金退款接口
    logger.info('押金退款接口--{}'.format(order_id))
    try:
        order = OrderInfo.objects.get(id=order_id)
    except Exception as e:
        logger.error('押金退款接口, 获取订单异常--{}'.format(e))
        return
    # 正常退押金 状态必为20+
    # if order.status <= 20:
    #     return

    reward_pay_order_list = PayOrder.objects.filter(order=order, order_type=1, status=3)
    logger.info('支付订单总数in line:{}'.format(reward_pay_order_list.count()))
    refund_status = paycenter_refund(reward_pay_order_list, refund_mes='退还押金')
    try:
        assert refund_status
        OrderOperateLog.logging(order=order, message='订单已完成, 退还押金')
    except Exception as e:
        logging.error('押金退款失败, 再次发起退款')
        raise self.retry(exc=e, countdown=60, max_retries=5)


@task(bind=True)
def order_complete_monitor(self, order_id):
    # 佣兵点击完成后
    logger.info('超时自动点击确认 任务')
    order_list = OrderInfo.objects.filter(id=order_id, status=21)
    logger.info('超时自动点击确认 任务id:{}, 总订单数:{}'.format(order_id, order_list.count()))
    for order in order_list:
        order.status = 50
        order.complete_time = timezone.now()
        order.save()
        OrderOperateLog.logging(order=order, message='雇主超时未点击确认, 订单自动完成')


@task(bind=True)
def order_create_send_email_notice(self, message, to_email):
    subject = '新订单提醒'
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        result = send_mail(subject, message, from_email, to_email, fail_silently=False)
        logging.info('邮件发送结果: {}-{}--结果{}'.format(from_email, to_email, result))
    except Exception as e:
        logging.error('邮件发送失败: {}-{}--结果{}--异常原因{}'.format(from_email, to_email, result, e))
