from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from .models import BalanceDetail, BankCard, WithDraw
from users.models import ProfileExtendInfo

User = get_user_model()


@receiver(post_save, sender=BalanceDetail)
def balance_detail_create(sender, instance=None, created=False, **kwargs):
    if created:
        if instance.balance > 0:
            profile_extend_instance = ProfileExtendInfo.objects.get(user=instance.user)
            profile_extend_instance.balance += instance.balance
            profile_extend_instance.save()
        else:
            profile_extend_instance = ProfileExtendInfo.objects.get(user=instance.user)
            profile_extend_instance.balance -= abs(instance.balance)
            profile_extend_instance.deposit_freeze += abs(instance.balance)
            profile_extend_instance.save()


@receiver(post_save, sender=BankCard)
def bank_card_create(sender, instance=None, created=False, **kwargs):
    if created:
        for user_one in User.objects.filter(id=instance.user.id):
            user_one.first_name = instance.name
            user_one.save()


@receiver(post_save, sender=WithDraw)
def with_draw_insert(sender, instance=None, created=False, **kwargs):
    if created:
        BalanceDetail.objects.create(
            user=instance.user,
            origin_type='30',
            order=instance.id,
            balance=instance.balance * -1
        )
    else:
        if instance.status == '2':
            profile_extend_instance = ProfileExtendInfo.objects.get(user=instance.user)
            profile_extend_instance.deposit_freeze -= abs(instance.balance)
            profile_extend_instance.save()
        elif instance.status == '3':
            profile_extend_instance = ProfileExtendInfo.objects.get(user=instance.user)
            profile_extend_instance.deposit_freeze -= abs(instance.balance)
            profile_extend_instance.balance += abs(instance.balance)
            profile_extend_instance.save()
