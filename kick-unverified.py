import discord
import pytz
import logging
from datetime import datetime, timedelta
import os

TOKEN = os.environ['DISCORD_BOT_TOKEN']
GUILD_NAME = os.environ['DISCORD_GUILD_NAME']
GUILD_ID = os.environ['DISCORD_GUILD_ID']
KICK_TIME_THRESHOLD = timedelta(minutes=15)
BAN_LIST = ["ZetaChain |", "MEE6"]

logging.basicConfig(level=logging.INFO)
intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    current_time = datetime.now(pytz.utc)
    ban_count = 0
    kick_count = 0
    for guild in client.guilds:
        if guild.name == GUILD_NAME or guild.id == GUILD_ID:
            logging.debug(
                f'{client.user} is running in the following server:\n{guild.name} (id: {guild.id})')

            # Iterate over each member and kick bots who can't verify
            for member in guild.members:
                try:
                    # Find members with a single role (@everyone only and no other role)
                    if len(member.roles) == 1:
                        logging.debug(
                            f"Member {member.name} (id: {member.id}) has no roles. Checking join time...")

                        # If this member has been in the server for more than {KICK_TIME_THRESHOLD} minutes
                        # and still has no roles, kick them
                        join_time = member.joined_at
                        time_since_join = current_time - join_time

                        if time_since_join > KICK_TIME_THRESHOLD:
                            try:
                                logging.debug(
                                    f"Member {member.name} (id: {member.id}) has been in the server for more than {KICK_TIME_THRESHOLD} without obtaining a role...")
                                # If their name matches known bots ban them for good measure
                                if any(ban_name.lower() in member.name.lower() for ban_name in BAN_LIST):
                                    logging.info(
                                        f"Banning Member {member.name} (id: {member.id}) for matching known bot name")
                                    await member.ban(reason="Name matches name used by bot attacks")
                                    ban_count += 1
                                # If it's not a known bot,just kick them in case it's a real user
                                else:
                                    logging.info(
                                        f"Kicking Member {member.name} (id: {member.id})")
                                    await member.kick()
                                    kick_count += 1

                            except Exception as e:
                                logging.error(
                                    f"An error occurred while kicking member {member.name} (id: {member.id}): {e}")
                                continue
                except Exception as e:
                    logging.error(
                        f"An error occurred while processing member {member.name} (id: {member.id}): {e}")
                    continue
            logging.info("--------------------")
            logging.info(f"Kicked {kick_count} members")
            logging.info(f"Banned {ban_count} members")
            break
    await client.close()


client.run(TOKEN)
