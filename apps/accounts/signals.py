from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from .models import BalanceDetail, BankCard
from users.models import ProfileExtendInfo

User = get_user_model()


@receiver(post_save, sender=BalanceDetail)
def balance_detail_insert(sender, instance=None, created=False, **kwargs):
    if created:
        profile_extend_instance = ProfileExtendInfo.objects.get(user=instance.user)
        profile_extend_instance.balance += instance.balance
        profile_extend_instance.save()


@receiver(post_save, sender=BankCard)
def balance_detail_insert(sender, instance=None, created=False, **kwargs):
    if created:
        for user_one in User.objects.filter(id=instance.user.id):
            user_one.first_name = instance.name
            user_one.save()
