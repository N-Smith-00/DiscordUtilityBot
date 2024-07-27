import discord


async def log(entry:discord.AuditLogEntry, channel:discord.TextChannel):
    match entry.action:
        case discord.AuditLogAction.kick:
            await channel.send(f"{entry.target.name} was kicked by {entry.user.name}\nReason: {entry.reason}")
        case discord.AuditLogAction.member_prune:
            await channel.send(f"Member prune initiated by {entry.user.name}\nLength: {entry.extra.delete_member_days}\nMembers removed: {entry.extra.members_removed}")