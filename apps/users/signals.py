import logging
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from users.models import ProfileExtendInfo
from recruit.models import Company


User = get_user_model()
logger = logging.getLogger('users')


@receiver(post_save, sender=User)
def user_extend_create(sender, instance=None, created=False, **kwargs):
    logger.debug('sender:{};instance:{};created:{}'.format(sender, instance, created))
    if created:
        try:
            ProfileExtendInfo.objects.create(user=instance)
        except Exception as e:
            logger.error('插入错误:{}'.format(e))


@receiver(post_save, sender=Company)
def user_admin_company(sender, instance=None, created=False, **kwargs):
    # 审核通过
    if instance.status == 30:
        # 只有操作者还没有管理企业时才插入
        if not instance.user.profileextendinfo.admin_company:
            instance.user.profileextendinfo.admin_company = instance
            instance.user.profileextendinfo.save()
