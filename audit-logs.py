
### Notes 
"""


# Add Bot to Server https://discordapp.com/oauth2/authorize?&client_id=1094923158714331296&scope=bot&permissions=268436614



A couple ways to do this Return all logs, filter down based on user and or
action after  -- very inefficient since we return all logs

Return logs on a per user basis. Step 1 - Get users, Step 2 - get logs, step 3
Analyzer/parse logs -- Better but we miss actions that ran by unexpected or
authroized users


Return logs by action -- Probaly the safest approach since we know the actions
we care about. Then we can parse the logs for the users and other details we
care about

Might need to categorize the actions we care about into buckets. For example - Sever/Admin actions, Mod Actions (things like deleting mesages, kick users etc


----

List of logged actions https://discord.com/developers/docs/resources/audit-log 

"""


### Notes End ####

import discord
import os
from datetime import datetime, timedelta
from collections import defaultdict
import csv

## Generate a Snowflake ID for a timestamp
# thirty_days_ago = datetime.now() - timedelta(days=30)
thirty_days_ago = datetime(2023, 6, 1)
snowflake_id = discord.utils.time_snowflake(thirty_days_ago)

## Create a discord.Object with this Snowflake ID
snowflake_object = discord.Object(id=snowflake_id)

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))  # Convert to int since environment variables are strings

MODERATOR_ROLE_IDS = [1111736117008531516, 1037485998856216586]  # IDs of moderator roles - VIP, Protectorate, etc
TEAM_ROLE_IDS = [902994157889523754]  # IDs of moderator roles - VIP, Protectorate, etc
ADMIN_ROLE_IDS = [902994157889523754]  # IDs of the roles you want to analyze

## Actions we care about
automod_actions = [
    discord.AuditLogAction.automod_block_message,
    discord.AuditLogAction.automod_timeout_member,
    discord.AuditLogAction.automod_flag_message,
]

moderator_actions = [
    discord.AuditLogAction.kick,
    discord.AuditLogAction.member_prune,
    discord.AuditLogAction.ban,
    discord.AuditLogAction.unban,
    discord.AuditLogAction.member_update,
    discord.AuditLogAction.member_role_update,
    discord.AuditLogAction.member_move,
    discord.AuditLogAction.member_disconnect,
    discord.AuditLogAction.invite_create,
    discord.AuditLogAction.invite_update,
    discord.AuditLogAction.invite_delete,
    discord.AuditLogAction.emoji_create,
    discord.AuditLogAction.emoji_update,
    discord.AuditLogAction.emoji_delete,
    discord.AuditLogAction.message_delete,
    discord.AuditLogAction.message_bulk_delete,
    discord.AuditLogAction.message_pin,
    discord.AuditLogAction.message_unpin,
    # discord.AuditLogAction.sticker_create,
    # discord.AuditLogAction.sticker_update,
    # discord.AuditLogAction.sticker_delete,
    # discord.AuditLogAction.thread_create,
    # discord.AuditLogAction.thread_update,
    # discord.AuditLogAction.thread_delete,
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
    discord.AuditLogAction.app_command_permission_update
]

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)

def create_list_by_action(audit_logs): # Not used
# Break out logs into different lists based on action
    automod_logs = []
    admin_logs = []
    moderator_logs = []
    extra_logs = []
    for log in audit_logs:
        try:
            if log.action in automod_actions:
                automod_logs.append(log)
                # print(f'Automod Action: {log}')
            elif log.action in moderator_actions:
                moderator_logs.append(log)
                # print(f'Moderator Action: {log}')
            elif log.action in admin_actions:
                admin_logs.append(log)
                # print(f'Admin Action: {log}')
            else:
                extra_logs.append(log)
            # if log.user is not None and any(role.id in (MODERATOR_ROLE_IDS + ADMIN_ROLE_IDS) for role in log.user.roles):
            #     filtered_logs.append(log)
        except AttributeError:
            print(f'Problematic log entry: {log}')

    print(f'Fetched {len(automod_logs)} automod_logs audit log entries')
    print(f'Fetched {len(moderator_actions)} moderator_actions audit log entries')
    print(f'Fetched {len(admin_actions)} admin_actions audit log entries')
    print(f'Fetched {len(extra_logs)} extra_logs audit log entries') # TODO - Get the unique actions and make sure they aren't something we care about 
async def top_users(action_counter, limit=10): # Not used

    for action, user_counts in action_counter.items():

        if action in admin_actions:
            # Sort the users by count for this action and take the first 10
            top_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            print(f"\nTop users for admins actions {action}:")
            
            for user_id, count in top_users:
                user = await client.fetch_user(user_id)
                print(f"User {user.name} has performed action {action} {count} times")
            
        elif action in moderator_actions:
            # Sort the users by count for this action and take the first 10
            top_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            print(f"\nTop users for moderator actions {action}:")
            
            for user_id, count in top_users:
                user = await client.fetch_user(user_id)
                print(f"User {user.name} has performed action {action} {count} times")
        elif action in automod_actions:
            # Sort the users by count for this action and take the first 10
            top_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            print(f"\nTop users for automode actions {action}:")
            
            for user_id, count in top_users:
                user = await client.fetch_user(user_id)
                print(f"User {user.name} has performed action {action} {count} times")    
        
def write_csv(user_data, filename='audit-log-report.csv'):
    try:
        with open(filename, 'w', newline='') as csvfile:
            # Create a CSV writer
            writer = csv.writer(csvfile)
            # Write the header
            writer.writerow(['User ID', 'Username', 'Action', 'Count', 'Is Moderator', 'Is Admin'])

            # Write the user data
            for user_id, data in user_data.items():
                for action, count in data['actions'].items():
                    writer.writerow([
                        user_id,
                        data['username'],
                        action,
                        count,
                        data['is_moderator'],
                        data['is_admin']
                    ])
    except Exception as e:
        print(f'Problem writing CSV: {e}')

def format_logs(audit_logs):
    try:
        user_data = {}
        # user_data = {user_id: {'actions': {action: count}, 'is_moderator': True/False, 'is_admin': True/False}}

        print(MODERATOR_ROLE_IDS)
        print(ADMIN_ROLE_IDS)
        for log in audit_logs:
            try:
                if log.action in (automod_actions + moderator_actions + admin_actions):
                    user_id = log.user.id
                    username = log.user
                    action = log.action
                    roles = [role.id for role in log.user.roles]

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
                    user_data[user_id]['actions'][action] = user_data[user_id]['actions'].get(action, 0) + 1

            except AttributeError:
                print(f'Problematic log entry: {log}')
                user_id = None
                if user_id not in user_data:
                    user_data[user_id] = {
                        'username': None,
                        'actions': {},
                        'is_moderator': any(role in roles for role in MODERATOR_ROLE_IDS),
                        'is_admin': any(role in roles for role in ADMIN_ROLE_IDS),
                    }
                # Increment the count for the action
                user_data[user_id]['actions'][action] = user_data[user_id]['actions'].get(action, 0) + 1
            except Exception as e:
                print(f'Problematic log entry: {log} - {e}')
        
        return user_data
    except Exception as e:
        print(f'Problem formatting logs: {e}')

async def get_audit_logs():
    try:
        print(f'Logged in as {client.user.name} ({client.user.id})')
        guild = discord.utils.get(client.guilds, id=GUILD_ID)
        if guild is None:
            print(f'Unable to find the guild with the ID {GUILD_ID}')
            return
        audit_logs = []
        async for entry in guild.audit_logs(limit=5000, after=snowflake_object):
            audit_logs.append(entry)
        print(f'Fetched {len(audit_logs)} audit log entries')
        return audit_logs
    except Exception as e:
        print(f'Problem fetching audit logs: {e}')
        exit()

@client.event
async def on_ready():


    # Fetch audit log entries

    audit_logs = await get_audit_logs()

    formatted_logs = format_logs(audit_logs)
    
    write_csv(formatted_logs)

    await client.close()


def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()