from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BalanceDetail
from users.models import ProfileExtendInfo


@receiver(post_save, sender=BalanceDetail)
def balance_detail_insert(sender, instance=None, created=False, **kwargs):
    if created:
        profile_extend_instance = ProfileExtendInfo.objects.get(user=instance.user)
        profile_extend_instance.balance += instance.balance
        profile_extend_instance.save()