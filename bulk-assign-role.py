import discord
import logging
import os
import csv

TOKEN = os.environ['DISCORD_BOT_TOKEN']
GUILD_NAME = os.environ['DISCORD_GUILD_NAME']
GUILD_ID = os.environ['DISCORD_GUILD_ID']
ROLE_ID = int(os.environ['DISCORD_ROLE_ID_FOR_ASSIGNMENT'])
USER_IDS_FILE = "user_ids.txt"

logging.basicConfig(level=logging.INFO)
intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD_NAME or guild.id == GUILD_ID:
            logging.debug(
                f'{client.user} is running in the following server:\n{guild.name} (id: {guild.id})')

            role = discord.utils.get(guild.roles, id=ROLE_ID)
            if not role:
                logging.error(f"Role with ID '{ROLE_ID}' not found in the server.")
                await client.close()
                return

            with open(USER_IDS_FILE, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    user_id = int(row[0])
                    member = guild.get_member(user_id)
                    if member:
                        try:
                            # await member.add_roles(role)
                            logging.info(f"Assigned role with ID '{ROLE_ID}' to member {member.name} (id: {member.id})")
                        except Exception as e:
                            logging.error(f"An error occurred while assigning role to member {member.name} (id: {member.id}): {e}")
                    else:
                        logging.warning(f"Member with id {user_id} not found in the server.")

    await client.close()


client.run(TOKEN)
