import discord
import os
import logging
import csv

TOKEN = os.environ['DISCORD_BOT_TOKEN']
GUILD_NAME = os.environ['DISCORD_GUILD_NAME']
FILENAME = "role-list.csv"

logging.basicConfig(level=logging.INFO)
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    with open(FILENAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Role Name", "Role ID"])

        for guild in client.guilds:
            if guild.name == GUILD_NAME:
                logging.debug(
                    f'{client.user} is running in the following server:\n{guild.name} (id: {guild.id})')
                roles = guild.roles
                for role in roles:
                    row = [role.name, role.id]
                    writer.writerow(row)
    
    await client.close()

def main():
    client.run(TOKEN)

main()
