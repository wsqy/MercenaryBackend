import logging
from django.utils import timezone
from celery import task
from django.core.mail import send_mail
from django.conf import settings

from .models import PartTimeOrder, PartTimeOrderCard, PartTimeOrderSignUp, PartTimeOrderCardSignUp
from paycenter.models import PartTimePayOrder
from utils.pay import alipay, wxpay
from utils.common import generate_random_number

logger = logging.getLogger('recruit')

def paycenter_refund(sign, refund_mes='订单退款'):
    try:
        reward_pay_order = PartTimePayOrder.objects.filter(order=sign, status=3)[0]
    except Exception as e:
        logger.info('查找支付订单失败: {}'.format(e))
        return True

    logger.info('{} 待退款--支付方式 {}'.format(reward_pay_order.id, reward_pay_order.pay_method))
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
def check_order_signup_status(self, sign_id, to_sign_status, refund_mes='订单退款'):
    sign = PartTimeOrderSignUp.objects.get(id=sign_id)
    if PartTimeOrderCardSignUp.objects.filter(sign=sign, status__gt=0).count() == 0:
        print('报名已经没有卡片了')
        has_pay = sign.recruit.deposit > 0 and sign.status > 10
        sign.status = to_sign_status
        sign.save()
        if has_pay:
            refund_status = paycenter_refund(sign, refund_mes)
            try:
                assert refund_status
            except Exception as e:
                logging.error('押金退款失败, 再次发起退款')
                raise self.retry(exc=e, countdown=60, max_retries=5)


@task(bind=True)
def recruit_cancel(self, recruit_id, refund_mes='商户取消兼职招募令退款'):
    recruit = PartTimeOrder.objects.get(id=recruit_id)
    recruit.status = -20
    recruit.save()
    PartTimeOrderCard.objects.filter(recruit=recruit).update(status=-10)
    PartTimeOrderCardSignUp.objects.filter(recruit=recruit, status__gt=0).update(status=-10)
    for sign in PartTimeOrderSignUp.objects.filter(recruit=recruit, status__gt=0):
        check_order_signup_status.apply_async(args=(sign.id, -10, refund_mes))