from django.dispatch import receiver
from vkontakte_api.signals import vkontakte_api_post_fetch #TODO проверить что есть такая штука
from vkontakte_groups.models import Group
from . models import Group


@receiver(vkontakte_api_post_fetch, sender=Group)
def group_statistic_create(sender, instance, **kwargs):
    if instance.members is None:
        return

    GroupStatisticMembers.objects.create(group=instance,
         members=instance.members)
