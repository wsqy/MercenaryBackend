from django.apps import AppConfig


class RecruitConfig(AppConfig):
    name = 'recruit'
    verbose_name = '招募令'

    def ready(self):
        import recruit.signals
