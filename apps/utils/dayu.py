# -*- coding: utf-8 -*-
import time
import json
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider


class DaYuSMS:
    DaYuSMS_STATUS = {
        'OK': '发送成功',
        'isp.RAM_PERMISSION_DENY': 'RAM权限DENY',
        'isv.OUT_OF_SERVICE': '发送成功',
        'isv.PRODUCT_UN_SUBSCRIPT': '未开通云通信产品的阿里云客户',
        'isv.isv.PRODUCT_UNSUBSCRIBE': '产品未开通',
        'isv.ACCOUNT_NOT_EXISTS': '账户不存在',
        'isv.ACCOUNT_ABNORMAL': '账户异常',
        'isv.SMS_TEMPLATE_ILLEGAL': '短信模板不合法',
        'isv.SMS_SIGNATURE_ILLEGAL': '短信签名不合法',
        'isv.INVALID_PARAMETERS': '参数异常',
        'isv.SYSTEM_ERROR': '系统错误',
        'isv.MOBILE_NUMBER_ILLEGAL': '非法手机号',
        'isv.MOBILE_COUNT_OVER_LIMIT': '手机号码数量超过限制',
        'isv.TEMPLATE_MISSING_PARAMETERS': '模板缺少变量',
        'isv.BUSINESS_LIMIT_CONTROL': '业务限流',
        'isv.INVALID_JSON_PARAM': 'JSON参数不合法，只接受字符串值',
        'isv.BLACK_KEY_CONTROL_LIMIT': '黑名单管控',
        'isv.PARAM_LENGTH_LIMIT': '参数超出长度限制',
        'isv.PARAM_NOT_SUPPORT_URL': '不支持URL',
        'isv.AMOUNT_NOT_ENOUGH': '黑名单管控',
        'isv.BLACK_KEY_CONTROL_LIMIT': '账户余额不足',
        'UNKNOWN_ERROR': '未知错误',
    }

    def __init__(self, ACCESS_KEY_ID, ACCESS_KEY_SECRET):
        self.__ACCESS_KEY_ID = ACCESS_KEY_ID
        self.__ACCESS_KEY_SECRET = ACCESS_KEY_SECRET
        self.REGION = 'cn-hangzhou'
        self.PRODUCT_NAME = 'Dysmsapi'
        self.DOMAIN = 'dysmsapi.aliyuncs.com'
        self.acs_client = AcsClient(self.__ACCESS_KEY_ID, self.__ACCESS_KEY_SECRET, self.REGION)
        region_provider.add_endpoint(self.PRODUCT_NAME, self.REGION, self.DOMAIN)

    def send_sms(self, business_id=None, phone_numbers=None, sign_name="雇佣兵", template_code=None, template_param=None):
        smsRequest = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        smsRequest.set_TemplateCode(template_code)

        # 短信模板变量参数
        if template_param is not None:
            smsRequest.set_TemplateParam(template_param)

        if business_id is None:
            business_id = time.time() * 10000000

        # 设置业务请求流水号，必填。
        smsRequest.set_OutId(business_id)

        # 短信签名
        smsRequest.set_SignName(sign_name)

        # 短信发送的号码列表，必填。
        smsRequest.set_PhoneNumbers(phone_numbers)

        # 调用短信发送接口，返回json
        smsResponse = self.acs_client.do_action_with_exception(smsRequest)

        return smsResponse


if __name__ == '__main__':
    params = {
        'code': '2245',
        'time': '3分钟'
    }
    phone = "184500982806"
    print(send_sms((time.time() * 10000000), phone, "雇佣兵", "SMS_76310006", json.dumps(params)))
