# coding: utf-8
# wxpay sdk https://github.com/wxpay/WXPay-SDK-Python

import time
import copy
import hmac
import string
import random
import hashlib
import xml.etree.ElementTree as ElementTree

import requests


def as_text(v):
    if v is None:
        return None
    elif isinstance(v, bytes):
        return v.decode('utf-8', errors='ignore')
    elif isinstance(v, str):
        return v
    else:
        raise ValueError('Unknown type %r' % type(v))


class WXPayConstants:
    # SUCCESS, FAIL
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'

    # 签名类型
    SIGN_TYPE_HMACSHA256 = 'HMAC-SHA256'
    SIGN_TYPE_MD5 = 'MD5'

    # 字段
    FIELD_SIGN = 'sign'
    FIELD_SIGN_TYPE = 'sign_type'

    # URL
    MICROPAY_URL = 'https://api.mch.weixin.qq.com/pay/micropay'
    UNIFIEDORDER_URL = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    ORDERQUERY_URL = 'https://api.mch.weixin.qq.com/pay/orderquery'
    REVERSE_URL = 'https://api.mch.weixin.qq.com/secapi/pay/reverse'
    CLOSEORDER_URL = 'https://api.mch.weixin.qq.com/pay/closeorder'
    REFUND_URL = 'https://api.mch.weixin.qq.com/secapi/pay/refund'
    REFUNDQUERY_URL = 'https://api.mch.weixin.qq.com/pay/refundquery'
    DOWNLOADBILL_URL = 'https://api.mch.weixin.qq.com/pay/downloadbill'
    REPORT_URL = 'https://api.mch.weixin.qq.com/payitil/report'
    SHORTURL_URL = 'https://api.mch.weixin.qq.com/tools/shorturl'
    AUTHCODETOOPENID_URL = 'https://api.mch.weixin.qq.com/tools/authcodetoopenid'


class WXPayUtil:

    @staticmethod
    def dict2xml(data):
        """dict to xml
        @:param data: Dictionary
        @:return: string
        """
        # return as_text( xmltodict.unparse({'xml': data_dict}, pretty=True) )
        root = ElementTree.Element('xml')
        for k in data:
            v = data[k]
            child = ElementTree.SubElement(root, k)
            child.text = str(v)
        return as_text(ElementTree.tostring(root, encoding='utf-8'))

    @staticmethod
    def xml2dict(xml_str):
        """xml to dict
        @:param xml_str: string in XML format
        @:return: Dictionary
        """
        # return xmltodict.parse(xml_str)['xml']
        root = ElementTree.fromstring(xml_str)
        assert as_text(root.tag) == as_text('xml')
        result = {}
        for child in root:
            tag = child.tag
            text = child.text
            result[tag] = text
        return result

    @staticmethod
    def generate_signature(unsigned_string, key, sign_type=WXPayConstants.SIGN_TYPE_MD5):
        """生成签名
        :param data: dict
        :param key: string. API key
        :param sign_type: string
        :return string
        """
        if sign_type == WXPayConstants.SIGN_TYPE_MD5:
            return WXPayUtil.md5(unsigned_string)
        elif sign_type == WXPayConstants.SIGN_TYPE_HMACSHA256:
            return WXPayUtil.hmacsha256(unsigned_string, key)
        else:
            raise Exception('Invalid sign_type: {}'.format(sign_type))

    @staticmethod
    def generate_nonce_str(len=32):
        """ 生成随机字符串
        :return string
        """
        return ''.join(random.sample(string.ascii_letters + string.digits, len))

    @staticmethod
    def md5(source):
        """ generate md5 of source. the result is Uppercase and Hexdigest.
        @:param source: string
        @:return: string
        """
        hash_md5 = hashlib.md5()
        hash_md5.update(source.encode('utf-8'))
        return hash_md5.hexdigest()

    @staticmethod
    def hmacsha256(source, key):
        """ generate hmacsha256 of source. the result is Uppercase and Hexdigest.
        @:param source: string
        @:param key: string
        @:return: string
        """
        return hmac.new(key.encode('utf-8'), source.encode('utf-8'), hashlib.sha256).hexdigest().upper()


class SignInvalidException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class WXPay:
    def __init__(self, app_id, mch_id, key):
        """ 初始化
        :param timeout: 网络请求超时时间，单位毫秒
        """
        self.app_id = app_id
        self.mch_id = mch_id
        self.key = key
        self.timeout = 8000
        self.sign_type = WXPayConstants.SIGN_TYPE_MD5

    def is_pay_success(self, notify_dict):
        if notify_dict.get('return_code') == WXPayConstants.SUCCESS and notify_dict.get('result_code') == 'SUCCESS':
            return True
        return False

    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign_data(self, data):
        new_data = copy.deepcopy(data)
        new_data.pop(WXPayConstants.FIELD_SIGN, None)
        # 排序后的字符串
        unsigned_items = self.ordered_data(new_data)
        unsigned_string = '&'.join('{0}={1}'.format(k, v) for k, v in unsigned_items if k and v)
        string_sign_temp = unsigned_string + '&key=' + self.key

        return WXPayUtil.generate_signature(string_sign_temp, self.key, self.sign_type).upper()

    def is_signature_valid(self, data):
        """支付结果通知中的签名是否合法
        :param data: dict
        :return: bool
        """
        if WXPayConstants.FIELD_SIGN not in data:
            return False
        sign = self.sign_data(data)
        if sign == data.get(WXPayConstants.FIELD_SIGN):
            return True
        return False

    def request_without_cert(self, url, data, timeout=None):
        """ 不带证书的请求
        :param url: string
        :param data: dict
        :param timeout: int. ms
        :return:
        """
        req_body = WXPayUtil.dict2xml(data).encode('utf-8')
        req_headers = {'Content-Type': 'application/xml'}
        _timeout = self.timeout if timeout is None else timeout
        resp = requests.post(url,
                             data=req_body,
                             headers=req_headers,
                             timeout=_timeout / 1000.0)
        resp.encoding = 'utf-8'
        return as_text(resp.text)

    def process_response_xml(self, resp_xml):
        """ 处理微信支付返回的 xml 格式数据
        :param resp_xml:
        :return:
        """
        resp_dict = WXPayUtil.xml2dict(as_text(resp_xml))

        if 'return_code' in resp_dict:
            return_code = resp_dict.get('return_code')
        else:
            raise Exception('no return_code in response data: {}'.format(resp_xml))

        if return_code in [WXPayConstants.FAIL, WXPayConstants.SUCCESS]:
            return resp_dict
        else:
            raise Exception('return_code value {} is invalid in response data: {}'.format(return_code, resp_xml))

    def unifiedorder(self, **kwargs):
        """ 统一下单
        :param data: dict
        :param timeout: int
        :return: dict
        """
        biz_content = {
            'appid': self.app_id,
            'mch_id': self.mch_id,
            'nonce_str': WXPayUtil.generate_nonce_str(),
            'device_info': 'WEB'
        }
        biz_content.update(kwargs)

        sign = self.sign_data(biz_content).upper()
        biz_content[WXPayConstants.FIELD_SIGN] = sign
        url = WXPayConstants.UNIFIEDORDER_URL
        resp_xml = self.request_without_cert(url, biz_content)
        get_order_id_res = self.process_response_xml(resp_xml)
        return get_order_id_res

    def app_pay(self, **kwargs):
        get_order_id_res = self.unifiedorder(**kwargs)

        biz_content = {
            'appid': self.app_id,
            'partnerid': self.mch_id,
            'prepayid': get_order_id_res.get('prepay_id'),
            'package': 'Sign=WXPay',
            'noncestr': WXPayUtil.generate_nonce_str(),
            'timestamp': int(time.time()),
        }
        sign = self.sign_data(biz_content)
        biz_content[WXPayConstants.FIELD_SIGN] = sign
        return biz_content

    def refund(self, data):
        """ 申请退款
        :param data: dict
        :param timeout: int
        :return: dict
        """
        return self.wxpay_common(WXPayConstants.REFUND_URL, data)


def test():
    wxpay = WXPay(
        app_id='wx11246b0732973381',
        mch_id='1486240842',
        key='m12MGa0wQvD8XdArznO9hecRxWiPpobK',
    )

    wxpay_resp_dict = wxpay.app_pay(body='测试商家-商品类目',
                                    out_trade_no=str(int(time.time())),
                                    total_fee=1,
                                    spbill_create_ip='123.12.12.123',
                                    trade_type='APP')
    return wxpay_resp_dict


if __name__ == '__main__':
    test()
