from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = 'order'
    verbose_name = '订单管理'

    def ready(self):
        import order.signals
