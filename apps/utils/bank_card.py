import requests
from django.conf import settings


def realname_authentication(acct_pan, acct_name, cert_id, phone_num,
                            appcode=settings.ALIPAY_MARKET_AUTH_APPCODE,
                            url='http://lundroid.market.alicloudapi.com/lianzhuo/verifi'):
    """
    名称	类型	是否必须	描述
    acct_name	STRING	可选	姓名
    acct_pan	STRING	必选	银行卡号
    cert_id	STRING	可选	身份证号码
    phone_num	STRING	可选	预留手机号
    """
    params = {
        'acct_pan': acct_pan,
        'acct_name': acct_name,
        'cert_id': cert_id,
        'phone_num': phone_num
    }

    headers = {
        'Authorization': 'APPCODE {}'.format(appcode)
    }

    with requests.get(url=url, params=params, headers=headers) as r:
        try:
            return r.json()
        except Exception as e:
            return {}


def test():
    res = realname_authentication(acct_name='祁缘',
                                  acct_pan='622908117844294518',
                                  phone_num='18450098280',
                                  cert_id='321023199408186437')
    print(res)
