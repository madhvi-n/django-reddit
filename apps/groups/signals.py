from django.db.models.signals import post_save
from django.dispatch import receiver
from groups.models import Group, GroupMember, MemberRequest
from groups.services import assign_permissions

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

@receiver(pre_save, sender=GroupMember)
def permissions_for_member_type(sender, instance, created, **kwargs):
    if created.id:
        assign_permissions(
            instance.member_type,
            instance.member,
            instance.group
        )
