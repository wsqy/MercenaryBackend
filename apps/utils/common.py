import time
import random


def generate_order_id(order_type='10'):
    data_dic = {
        'order_type': order_type,
        'time_str': time.strftime('%Y%m%d%H%M%S'),
        'random_str': random.randint(1000, 9999),
    }
    return '{order_type}{time_str}{random_str}'.format(**data_dic)


def generate_pay_order_id(status='3', order_type='10'):
    """
    :param status: 3赏金1押金2加赏
    :param order_type:
    :return:
    """
    data_dic = {
        'status': status,
        'order_type': order_type,
        'time_str': time.strftime('%Y%m%d%H%M%S'),
        'random_str': random.randint(1000, 9999),
    }
    return '{status}{order_type}{time_str}{random_str}'.format(**data_dic)
