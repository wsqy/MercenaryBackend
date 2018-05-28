from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = '账户管理'

    def ready(self):
        import accounts.signals
