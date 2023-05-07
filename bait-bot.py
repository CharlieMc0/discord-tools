import requests
import json
import os
from threading import Thread

TOKEN = os.environ['DISCORD_USER_TOKEN']


# def join_guild(guild_id):

#     # The payload to add the bot to the server
#     payload = {
#         'access_token': TOKEN,
#         'nick': 'MyBot'
#     }

#     # Make the request to add the bot to the server
#     response = requests.put(f'https://discord.com/api/v9/guilds/{GUILD_ID}/members/{BOT_ID}', headers={
#                             'Authorization': f'Bot {TOKEN}'}, json=payload)

#     # Print the response to see if the bot was added successfully
#     print(response.json())


def report_first_dm(channel_id, message_id):

    # The headers contain your Discord token and the content type
    headers = {
        "Authorization": f"{TOKEN}",
        "Content-Type": "application/json"
    }

    # The payload contains the reason for the report
    payload = {"version": "1.0",
               "variant": "1",
               "language": "en",
               "breadcrumbs": [32],
               "elements": {},
               "name": "first_dm",
               "channel_id": channel_id,
               "message_id": message_id}

    # Make the request to suppress the message
    response = requests.post(
        "https://discord.com/api/v9/reporting/first_dm",
        headers=headers,
        json=payload
    )

    # Print the response to see if the report was successful
    print(response.json())


def get_dm_channels():
    response = requests.get(
        "https://discord.com/api/users/@me/channels",
        headers={"Authorization": f"{TOKEN}"}
    )
    channels = response.json()
    return channels


def read_messages(channels):
    # Loop through DM channels and download messages
    for channel in channels:
        channel_id = channel["id"]
        response = requests.get(
            f"https://discord.com/api/channels/{channel_id}/messages",
            headers={"Authorization": f"{TOKEN}"}
        )
        messages = response.json()

        for message in messages:
            message_id = message['id']
            channel_id = message['channel_id']
            print(f"Message ID: {message_id}")
            print(f"Channel ID: {channel_id}")
            print(f"Author ID: {message['author']['id']}")
            print(f"Author Username: {message['author']['username']}")

            # Report It
            # report_first_dm(channel_id, message_id)

        # Write messages to file
        with open(f"{channel_id}.json", "w") as f:
            json.dump(messages, f)


channels = get_dm_channels()
read_messages(channels)
