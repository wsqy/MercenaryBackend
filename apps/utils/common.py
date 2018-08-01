import time
import random
import string


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


def get_request_ip(request, must=False):
    """
    从请求中获取ip,
    :param request:
    :param must:  must参数为true 将会返回'1.1.1.1'代替获取不到请求的ip
    :return:
    """
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', '')
    else:
        client_ip = request.META.get('REMOTE_ADDR', '')
    if client_ip == '' and must:
        client_ip = '1.1.1.1'
    return client_ip


def generate_random_str(length=32):
    """
    生成指定长度的随机字符串
    :param length:
    :return:
    """
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


def generate_random_number(length=4):
    """
    生成指定长度的随机数字
    :param length:
    :return:
    """
    return ''.join(random.sample(string.digits, length))


def to_number(num):
    try:
        return float(num)
    except:
        return 0


def response_data_group(response_data, group_element):
    """
    将响应数据分组并包含每个分组的数量
    :param data: 原始数据
    :param group_element: 分组属性
    :return:
    """
    res_data = {}
    for data in response_data:
        group = data.get(group_element)
        if group in res_data:
            res_data[group]['results'].append(data)
            res_data[group]['count'] += 1
        else:
            res_data[group] = {
                'results': [data,],
                'count': 1
            }
    return res_data
