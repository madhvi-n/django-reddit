from django.db.models.signals import post_save
from django.dispatch import receiver
from groups.models import Group, GroupMember, MemberRequest


@receiver(post_save, sender=MemberRequest)
def member_request_created_hook(sender, instance, created, **kwargs):
    if created:
        if instance.group.group_type == Group.group_type.PUBLIC:
            instance.is_approved = True
            instance.save()
            member, created = GroupMember.objects.create(
                group=instance.group,
                user=instance.user
            )
