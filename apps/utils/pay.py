from django.conf import settings

from alipay import AliPay


alipay = AliPay(
    appid=settings.ALIPAY_APPID,
    app_notify_url=ALIPAY_NOTIFY_URL,
    app_private_key_path=ALIPAY_PRIVATE_KEY_PATH,
    alipay_public_key_path=ALIPAY_ALI_PUBLIC_KEY_PATH,
    debug=True,  # 默认False,
    return_url=ALIPAY_RETURN_URL,
)

