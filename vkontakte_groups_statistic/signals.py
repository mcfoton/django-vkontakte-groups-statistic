from django.dispatch import receiver
from vkontakte_api.signals import vkontakte_api_post_fetch
from vkontakte_groups.models import Group
from . models import GroupStatisticMembers


@receiver(vkontakte_api_post_fetch, sender=Group)
def group_statistic_create(sender, instance, **kwargs):
    if instance.members_count is None:
        return

    GroupStatisticMembers.objects.create(group=instance,
         members_count=instance.members_count)
