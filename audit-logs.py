
# Add Bot to Server https://discordapp.com/oauth2/authorize?&client_id=1094923158714331296&scope=bot&permissions=268436614
# List of logged actions https://discord.com/developers/docs/resources/audit-log

import discord
import os
from datetime import datetime, timedelta
from collections import defaultdict
import csv

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))

MODERATOR_ROLE_IDS = [1111736117008531516, 1037485998856216586]
TEAM_ROLE_IDS = [902994157889523754]
ADMIN_ROLE_IDS = [902994157889523754]

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)


## Actions we want to report on

automod_actions = [
    # discord.AuditLogAction.automod_block_message,
    # discord.AuditLogAction.automod_timeout_member,
    # discord.AuditLogAction.automod_flag_message,
]

moderator_actions = [
    discord.AuditLogAction.kick,  # Large Number Of Records
    discord.AuditLogAction.ban,
    discord.AuditLogAction.unban,
    discord.AuditLogAction.member_update,
    discord.AuditLogAction.member_role_update,  # Large Number Of Records
    discord.AuditLogAction.member_move,
    discord.AuditLogAction.member_disconnect,
    # discord.AuditLogAction.invite_create,
    # discord.AuditLogAction.invite_update,
    # discord.AuditLogAction.invite_delete,
    discord.AuditLogAction.emoji_create,
    discord.AuditLogAction.emoji_update,
    discord.AuditLogAction.emoji_delete,
    discord.AuditLogAction.message_delete,
    discord.AuditLogAction.message_bulk_delete,
    discord.AuditLogAction.message_pin,
    discord.AuditLogAction.message_unpin,
    discord.AuditLogAction.sticker_create,
    discord.AuditLogAction.sticker_update,
    discord.AuditLogAction.sticker_delete,
    discord.AuditLogAction.thread_create,
    discord.AuditLogAction.thread_update,
    discord.AuditLogAction.thread_delete,
]

admin_actions = [
    discord.AuditLogAction.guild_update,
    discord.AuditLogAction.channel_create,
    discord.AuditLogAction.channel_update,
    discord.AuditLogAction.channel_delete,
    discord.AuditLogAction.overwrite_create,
    discord.AuditLogAction.overwrite_update,
    discord.AuditLogAction.overwrite_delete,
    discord.AuditLogAction.bot_add,
    discord.AuditLogAction.role_create,
    discord.AuditLogAction.role_update,
    discord.AuditLogAction.role_delete,
    discord.AuditLogAction.webhook_create,
    discord.AuditLogAction.webhook_update,
    discord.AuditLogAction.webhook_delete,
    discord.AuditLogAction.integration_create,
    discord.AuditLogAction.integration_update,
    discord.AuditLogAction.integration_delete,
    discord.AuditLogAction.stage_instance_create,
    discord.AuditLogAction.stage_instance_update,
    discord.AuditLogAction.stage_instance_delete,
    discord.AuditLogAction.scheduled_event_create,
    discord.AuditLogAction.scheduled_event_update,
    discord.AuditLogAction.scheduled_event_delete,
    discord.AuditLogAction.app_command_permission_update,
    discord.AuditLogAction.member_prune,
]


async def get_audit_logs(start_date: datetime, end_date: datetime):
    try:
        print(f'Logged in as {client.user.name} ({client.user.id})')
        guild = discord.utils.get(client.guilds, id=GUILD_ID)
        if guild is None:
            print(f'Unable to find the guild with the ID {GUILD_ID}')
            return

        audit_logs = []

        # convert date into Snowflake ID
        start_snowflake_id = discord.utils.time_snowflake(start_date)
        end_snowflake_id = discord.utils.time_snowflake(end_date)
        start_snowflake_object = discord.Object(id=start_snowflake_id)
        end_snowflake_object = discord.Object(id=end_snowflake_id)

        for action in admin_actions + moderator_actions:  # automod_actions # moderator_actions,
            try:
                print(f'Total {len(audit_logs)} audit logs records so far...')
                print(f'Fetching audit logs for {action}...')

                async for entry in guild.audit_logs(limit=None, action=action, after=start_snowflake_object, before=end_snowflake_object):
                    audit_logs.append(entry)
                print(f'Fetched audit logs for {action}...')

            except Exception as e:
                print(f'Problem fetching audit logs for {action}: {e}')
                raise Exception

        print(f'Completed - Fetched {len(audit_logs)} audit logs')
        return audit_logs
    except Exception as e:
        print(f'Problem fetching audit logs: {e}')
        exit()


def write_csv(user_data, filename='audit-log-report.csv'):
    try:
        with open(filename, 'w', newline='') as csvfile:
            # Create a CSV writer
            writer = csv.writer(csvfile)
            # Write the header
            writer.writerow(['User ID', 'Username', 'Action',
                            'Is Moderator', 'Is Admin', 'Is Team', 'Count'])

            # Write the user data
            for user_id, data in user_data.items():
                for action, count in data['actions'].items():
                    writer.writerow([
                        user_id,
                        data['username'],
                        action,
                        data['is_moderator'],
                        data['is_admin'],
                        data['is_team'],
                        count
                    ])
    except Exception as e:
        print(f'Problem writing CSV: {e}')


def process_logs(audit_logs):
    try:
        user_data = {}  # {user_id: {'actions': {action: count}, 'is_moderator': True/False, 'is_admin': True/False, is_team: True/False}}

        for log in audit_logs:
            try:
                if log.action in (automod_actions + moderator_actions + admin_actions):
                    user_id = log.user.id
                    username = getattr(log, 'user', None)
                    action = log.action
                    roles = [role.id for role in log.user.roles] if getattr(
                        log.user, 'roles', None) else []

                    # If the user is not already in the dictionary, add them
                    if user_id not in user_data:
                        user_data[user_id] = {
                            'username': username,
                            'actions': {},
                            'is_moderator': any(role in roles for role in MODERATOR_ROLE_IDS),
                            'is_admin': any(role in roles for role in ADMIN_ROLE_IDS),
                            'is_team': any(role in roles for role in TEAM_ROLE_IDS),
                        }

                    # Increment the count for the action
                    user_data[user_id]['actions'][action] = user_data[user_id]['actions'].get(
                        action, 0) + 1

            except AttributeError as e:
                print(f'AttributeError: Processing log entry: {log}')
                raise AttributeError

            except Exception as e:
                print(f'Error: Processing log entry: {log}')
                raise Exception

        return user_data
    except Exception as e:
        print(f'Problem formatting logs: {e}')


@client.event
async def on_ready():

    start_date = datetime(2023, 6, 1)
    end_date = datetime(2023, 6, 30)

    audit_logs = await get_audit_logs(start_date, end_date)

    formatted_logs = process_logs(audit_logs)

    report_name = f"audit-log-report-{start_date.strftime('%Y-%m-%d')}-{end_date.strftime('%Y-%m-%d')}.csv"

    write_csv(formatted_logs, report_name)

    await client.close()


def main():
    client.run(TOKEN)


if __name__ == '__main__':
    main()
