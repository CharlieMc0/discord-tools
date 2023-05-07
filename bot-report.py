import discord
import os
import logging
import csv

TOKEN = os.environ['DISCORD_BOT_TOKEN']
GUILD_ID = os.environ['DISCORD_GUILD_ID']
GUILD_NAME = os.environ['DISCORD_GUILD_NAME']
FILENAME = "bot-report.csv"

logging.basicConfig(level=logging.INFO)
intents = discord.Intents.all()
client = discord.Client(intents=intents)


def print_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)


@client.event
async def on_ready():
    with open(FILENAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Bot Name", "Create Instant Invite", "Kick Members", "Ban Members", "Administrator", "Manage Channels", "Manage Guild", "Add Reactions", "View Audit Log", "Priority Speaker", "Stream", "View Channel", "Send Messages", "Send TTS Messages", "Manage Messages", "Embed Links",
                        "Attach Files", "Read Message History", "Mention Everyone", "Use External Emojis", "View Guild Insights", "Connect", "Speak", "Mute Members", "Deafen Members", "Move Members", "Use Voice Activation", "Change Nickname", "Manage Nicknames", "Manage Roles", "Manage Webhooks", "Manage Emojis"])

        for guild in client.guilds:
            if guild.name == GUILD_NAME or guild.id == GUILD_ID:
                logging.debug(
                    f'{client.user} is running in the following server:\n{guild.name} (id: {guild.id})')
                bots = [member for member in guild.members if member.bot]
                for bot in bots:
                    permissions = bot.guild_permissions
                    bot_name = bot.name
                    row = [bot_name, permissions.create_instant_invite, permissions.kick_members, permissions.ban_members, permissions.administrator, permissions.manage_channels, permissions.manage_guild, permissions.add_reactions, permissions.view_audit_log, permissions.priority_speaker, permissions.stream, permissions.view_channel, permissions.send_messages, permissions.send_tts_messages, permissions.manage_messages, permissions.embed_links,
                           permissions.attach_files, permissions.read_message_history, permissions.mention_everyone, permissions.use_external_emojis, permissions.view_guild_insights, permissions.connect, permissions.speak, permissions.mute_members, permissions.deafen_members, permissions.move_members, permissions.use_voice_activation, permissions.change_nickname, permissions.manage_nicknames, permissions.manage_roles, permissions.manage_webhooks, permissions.manage_emojis]
                    writer.writerow(row)
    await client.close()


def main():
    client.run(TOKEN)
    # print_csv(FILENAME)


main()
