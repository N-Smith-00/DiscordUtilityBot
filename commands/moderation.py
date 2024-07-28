import discord


async def log(client:discord.Client, entry:discord.AuditLogEntry, channel:discord.TextChannel):
    match entry.action:
        case discord.AuditLogAction.kick:
            print("kick")
            await channel.send(f"{client.get_user(entry.target.id)} was kicked by {client.get_user(entry.user_id)}\nReason: {entry.reason}")
        case discord.AuditLogAction.member_prune:
            print("prune")
            await channel.send(f"Member prune initiated by {client.get_user(entry.user_id)}\nLength: {entry.extra.delete_member_days} days\nMembers removed: {entry.extra.members_removed}")