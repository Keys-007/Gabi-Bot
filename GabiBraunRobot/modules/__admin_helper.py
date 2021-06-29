@register(outgoing=True, group_only=True, pattern="^.promote(?: |$)(.*)")
@grp_exclude()
async def promote(promt):
    """For .promote command, do promote targeted person"""
    # Get targeted chat
    chat = await promt.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, also return
    if not admin and not creator:
        await promt.edit(NO_ADMIN)
        return

    new_rights = ChatAdminRights(
        add_admins=admin.add_admins,
        invite_users=admin.invite_users,
        change_info=admin.change_info,
        ban_users=admin.ban_users,
        delete_messages=admin.delete_messages,
        pin_messages=admin.pin_messages,
    )

    await promt.edit("`Promoting...`")

    user = await get_user_from_event(promt)
    if user:
        pass
    else:
        return

    # Try to promote if current user is admin or creator
    try:
        await promt.client(
            EditAdminRequest(promt.chat_id, user.id, new_rights, "Admin")
        )
        await promt.edit("`Promoted!`")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        await promt.edit(NO_PERM)
        return

    # Announce to the logging group if we have promoted successfully
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID,
            "#PROMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {promt.chat.title}(`{promt.chat_id}`)",
        )
