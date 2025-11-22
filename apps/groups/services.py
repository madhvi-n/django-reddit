from groups.models import Group, GroupMember
from guardian.shortcuts import assign_perm, remove_perm


def assign_permissions(member_type, user, group):
    if member_type == GroupMember.MemberTypes.MEMBER.value:
        return
    elif member_type == GroupMember.MemberTypes.MODERATOR.value:
        assign_perm("add_members", user, group)
        assign_perm("edit_groups", user, group)
    elif member_type == GroupMember.MemberTypes.ADMIN.value:
        assign_permissions(GroupMember.MemberTypes.MODERATOR.value, user, group)
        assign_perm("add_moderators", user, group)
        assign_perm("remove_moderators", user, group)
        assign_perm("change_members", user, group)
        assign_perm("delete_members", user, group)
        assign_perm("delete_groups", user, group)
