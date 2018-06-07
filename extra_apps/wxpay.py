# coding: utf-8
# wxpay sdk https://github.com/wxpay/WXPay-SDK-Python

import sys
import copy
import hmac
import string
import random
import pprint
import hashlib
from urllib.parse import quote_plus

import xml.etree.ElementTree as ElementTree

text_type = str
string_types = (str,)
xrange = range


def as_text(v):  ## 生成unicode字符串
    if v is None:
        return None
    elif isinstance(v, bytes):
        return v.decode('utf-8', errors='ignore')
    elif isinstance(v, str):
        return v
    else:
        raise ValueError('Unknown type %r' % type(v))


def is_text(v):
    return isinstance(v, text_type)


class WXPayConstants(object):
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


class WXPayUtil(object):

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
    def is_signature_valid(data, key, sign_type=WXPayConstants.SIGN_TYPE_MD5):
        """ 验证xml中的签名
        :param data: dict
        :param key: string. API key
        :param sign_type: string
        :return: bool
        """
        if WXPayConstants.FIELD_SIGN not in data:
            return False
        sign = WXPayUtil.generate_signature(data, key, sign_type)
        if sign == data[WXPayConstants.FIELD_SIGN]:
            return True
        return False

    @staticmethod
    def generate_signed_xml(data, key, sign_type=WXPayConstants.SIGN_TYPE_MD5):
        """ 生成带有签名的xml
        :param data: dict
        :param key: string. API key
        :param sign_type: string
        :return: xml
        """
        key = as_text(key)
        new_data_dict = copy.deepcopy(data)
        sign = WXPayUtil.generate_signature(data, key, sign_type)
        new_data_dict[WXPayConstants.FIELD_SIGN] = sign
        return WXPayUtil.dict2xml(new_data_dict)

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
        hash_md5.update(source)
        return hash_md5.hexdigest()

    @staticmethod
    def hmacsha256(source, key):
        """ generate hmacsha256 of source. the result is Uppercase and Hexdigest.
        @:param source: string
        @:param key: string
        @:return: string
        """
        return hmac.new(key.encode('utf-8'), source.encode('utf-8'),
                        hashlib.sha256).hexdigest().upper()


class SignInvalidException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class WXPay(object):

    def __init__(self, app_id, mch_id, key):
        """ 初始化
        :param timeout: 网络请求超时时间，单位毫秒
        """
        self.app_id = app_id
        self.mch_id = mch_id
        self.key = key
        self.timeout = 8000
        self.sign_type = WXPayConstants.SIGN_TYPE_MD5

    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string, key, sign_type):
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

    def sign_data(self, data):
        new_data = copy.deepcopy(data)
        new_data.pop('sign', None)
        # 排序后的字符串
        unsigned_items = self.ordered_data(new_data)
        unsigned_string = '&'.join('{0}={1}'.format(k, v) for k, v in unsigned_items)
        string_sign_temp = unsigned_string + '&key=' + self.key
        pprint.pprint("string_sign_temp")
        pprint.pprint(string_sign_temp)
        pprint.pprint("string_sign_temp")
        return self.sign(string_sign_temp.encode('utf-8'), self.key, self.sign_type)

    def is_response_signature_valid(self, data):
        """检查微信响应的xml数据中签名是否合法，先转换成dict
        :param data: dict类型
        :return: bool
        """
        return WXPayUtil.is_signature_valid(data, self.key, self.sign_type)

    def is_pay_result_notify_signature_valid(self, data):
        """支付结果通知中的签名是否合法
        :param data: dict
        :return: bool
        """
        sign_type = data.get(WXPayConstants.FIELD_SIGN, WXPayConstants.SIGN_TYPE_MD5)
        if len(sign_type.trim()) == 0:
            sign_type = WXPayConstants.SIGN_TYPE_MD5
        if sign_type not in [WXPayConstants.SIGN_TYPE_MD5, WXPayConstants.SIGN_TYPE_HMACSHA256]:
            raise Exception('invalid sign_type: {} in pay result notify'.format(sign_type))
        return WXPayUtil.is_signature_valid(data, self.key, sign_type)

    def process_response_xml(self, resp_xml):
        """ 处理微信支付返回的 xml 格式数据
        :param resp_xml:
        :return:
        """
        resp_dict = WXPayUtil.xml2dict(resp_xml)
        if 'return_code' in resp_dict:
            return_code = resp_dict.get('return_code')
        else:
            raise Exception('no return_code in response data: {}'.format(resp_xml))

        if return_code == WXPayConstants.FAIL:
            return resp_dict
        elif return_code == WXPayConstants.SUCCESS:
            if self.is_response_signature_valid(resp_dict):
                return resp_dict
            else:
                raise SignInvalidException('invalid sign in response data: {}'.format(resp_xml))
        else:
            raise Exception('return_code value {} is invalid in response data: {}'.format(return_code, resp_xml))

    def wxpay_common(self, url, **kwargs):
        biz_content = {
            'appid': self.app_id,
            'mch_id': self.mch_id,
            'nonce_str': WXPayUtil.generate_nonce_str(),
            'sign_type': self.sign_type
        }
        biz_content.update(kwargs)

        sign = self.sign_data(biz_content)
        biz_content['sign'] = sign.upper()
        req_body = WXPayUtil.dict2xml(dict(biz_content))
        pprint.pprint("req_body")
        pprint.pprint(req_body)
        pprint.pprint("req_body")
        return req_body

    def unifiedorder(self, **kwargs):
        """ 统一下单
        :param data: dict
        :param timeout: int
        :return: dict
        """
        url = WXPayConstants.UNIFIEDORDER_URL
        return self.wxpay_common(url, **kwargs)

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
        key='c00d3d0c01b5c2535aee7ecf0614c712',
    )

    wxpay_resp_dict = wxpay.unifiedorder(device_info='WEB',
                                         body='测试商家-商品类目',
                                         detail='11111',
                                         out_trade_no='2016090910595900000012',
                                         total_fee=1,
                                         fee_type='CNY',
                                         notify_url='http://www.example.com/wxpay/notify',
                                         spbill_create_ip='123.12.12.123',
                                         trade_type='APP')
    return wxpay_resp_dict


if __name__ == '__main__':
    test()
