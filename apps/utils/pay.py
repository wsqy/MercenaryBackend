from django.conf import settings

from alipay import AliPay


alipay = AliPay(
    appid=settings.ALIPAY_APPID,
    app_notify_url=settings.ALIPAY_NOTIFY_URL,
    app_private_key_path=settings.ALIPAY_PRIVATE_KEY_PATH,
    alipay_public_key_path=settings.ALIPAY_ALI_PUBLIC_KEY_PATH,
    return_url=settings.ALIPAY_RETURN_URL,
)

