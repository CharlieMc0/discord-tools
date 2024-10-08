# discord-tools 
Collection of scripts for discord -- security audit, kick unverified users, etc  

These were developed with Python3 on a Mac and I have not tested them on other platforms. 

## bot-report.py 
This script will generate a report of all the permissions for all the
bots/integrations in a server and export them as a CSV.

For this script to work you must have connected your bot to the server with proper permissions

## kick-unverified.py 
This script will kick all users who have not received a role within a specified
number of minutes. You can also ban them if their username contains a specific
string. For example, kick any unverified users but ban anyone with "AIRDROP
SCAM" in the username. 

For this script to work you must have connected your bot to the server with proper permissions

## Bulk Assign 
This takes an list of discord user Ids as an input and assigns a new role to them. Role is specificed with env variable - DISCORD_ROLE_ID_FOR_ASSIGNMENT or you can edit value in the script. 