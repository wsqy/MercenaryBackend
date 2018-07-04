from django.conf import settings


class ServiceCostCalculation:
    """
    手续费计算
    """
    def __init__(self):
        self.service_cost = settings.SERVICE_COST
        self.recruit_deposit_cost = settings.RECRUIT_DEPOSIT_COST
        self.recruit_commission_cost = settings.RECRUIT_COMMISSION_COST

    def service_calc(self, pay_cost):
        """
        跑腿单佣金计算
        :param pay_cost:
        :return:
        """
        return round(pay_cost * self.service_cost / 100)

    def recruit_deposit_calc(self, wages):
        """
        根据工资计算押金
        :param wages:
        :return:
        """
        return round(wages * self.recruit_deposit_cost / 100)

    def recruit_commission_calc(self, wages, num):
        """
        根据工资计算我方应得佣金
        :param wages:
        :return:
        """
        return round(wages * self.recruit_commission_cost / 100 * num)


service_cost_calc = ServiceCostCalculation()
