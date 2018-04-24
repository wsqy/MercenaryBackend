from django.conf import settings


class ServiceCostCalculation:
    """
    手续费计算
    """
    def __init__(self):
        self.service_cost = settings.SERVICE_COST

    def calc(self, pay_cost):
        return round(pay_cost * self.service_cost / 100)


service_cost_calc = ServiceCostCalculation()
