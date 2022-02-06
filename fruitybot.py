import discord
from dotenv import load_dotenv
from discord.utils import get
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import ast
import re
import subprocess

scope = [
    "https://spreadsheets.google.com/feeds",
    'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Assign credentials an path of style sheet
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Database Fruity Bot").sheet1

load_dotenv()
TOKEN1 = 'ODg2MzM2NjU0MzkzMTEwNTY5.YT0HVQ.r0CKPWLQQsfKSJJfn7RpHGYWfk'
TOKEN = 'ODQ3NDg4NDU3MjQ4MDc5OTIz.YK-zIQ.3kq6hn_dAD61NdVuE5eMkXEwxs0'
GUILD = 'Fruity Bot'

client = discord.Client()


@client.event
async def on_ready():
  global carrot, elaine, kb, darlene, botSetup, hwPosting, my_date, listenMsg, linkResponders, linkRespondersKey, listenTrig, valueTrig, bannedwords, logChannel
  bannedwords = open('bad-words.txt').read().splitlines()
  listenMsg = False
  listenTrig = False
  logChannel = client.get_channel(879132756213370971)
  valueTrig = ''
  linkResponders = {
      '!hotg':
          'https://www.youtube.com/watch?v=9cwFmcJMayA',
      '!air1':
          'https://www.youtube.com/watch?v=b5DPLAYpjMI',
      '!air2':
          'https://www.youtube.com/watch?v=yZHUimkhRFA',
      '!air1ly':
          '<https://genius.com/Chickbait-siri-vs-alexa-ai-rap-battle-lyrics>',
      '!nofriends':
          'https://www.youtube.com/watch?v=FfAjtZgLkPQ',
      '!supercool':
          '<https://www.youtube.com/watch?v=dQw4w9WgXcQ>'
  }
  linkRespondersKey = linkResponders.keys()

  for guild in client.guilds:
    if guild.name == GUILD:
      break
    
  

  print(f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n')
  print("Fruity Bot's Ready!")


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  global carrot, elaine, kb, darlene, botSetup, hwPosting, my_date, listenMsg, linkResponders, linkRespondersKey, listenTrig, valueTrig, bannedwords, logChannel
  
  

  userMsg: str = str(message.content)
  messageChannel = str(message.channel)
  messageAuthor = str(message.author)
  messageLink = f'https://discordapp.com/channels/{message.guild.id}/{message.channel.id}/{message.id}'
  authorDiscrimator = message.author.discriminator
  serverName = message.guild.name
  serverID = message.guild.id
  channelID = message.channel.id
  authorID = message.author.id
  postedByBot = message.author.bot
  autoresponderData = ast.literal_eval(sheet.cell(2, 1).value)
  triggerKeys = autoresponderData.keys()


  # print(f"""
  # Message: {userMsg}
  # Channel: {messageChannel}
  # Channel ID: {channelID}
  # Author: {messageAuthor}
  # Author ID: {authorID}
  # Author Discrimator: {authorDiscrimator}
  # Server: {serverName}
  # Server ID: {serverID}
  # Posted By Bot: {postedByBot}""")
  if not postedByBot:
    print(F"{messageAuthor}: {userMsg}")
  # sesnored words
  # for i in userMsg.split(' '):
  #   if i in bannedwords:
  #     await message.channel.send(f'OOPS <@!{authorID}> said a banned word!')
  #     await message.channel.send(f'assigining mute role now....')
  #     role = discord.utils.get(message.guild.roles, id=919092841408524319)
  #     await message.author.add_roles(role)
  #     # embed = discord.Embed(
  #     # title=f"Banned Word Encounter | {messageAuthor}",
  #     # url=messageLink,
  #     # description=f"Banned word ({i}) in #{messageChannel}",
  #     # color=0xFF0000)
  #     embed=discord.Embed(title=f"Mute | {messageAuthor}", color=0xff0000)
  #     embed.set_author(name="Fruity Bot", url=messageLink, icon_url="https://cdn.discordapp.com/avatars/886336654393110569/a1b72f8b61f977998872140bab0d9f1a.png?size=80")
  #     embed.add_field(name="Offender", value=messageAuthor, inline=True)
  #     embed.add_field(name="Blacklisted Word", value=i, inline=True)
  #     await logChannel.send(embed=embed)


  # purge
  if userMsg.startswith('!purge'):
    amount=int(userMsg[6:])
    channel = message.channel
    messages = []
    async for message in channel.history(limit=amount + 1):
              messages.append(message)
    await message.channel.delete_messages(messages)
    await message.channel.send(f'{amount} messages have been purged by {message.author.mention}')

  # ping command
  if userMsg.startswith('!ping'):
    embed = discord.Embed(
        title="Ping",
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        description=f"My ping is {round(client.latency, 3)*1000}ms!",
        color=0xFF5733)
    await message.channel.send(embed=embed)

  #subprocess
  if userMsg.startswith('!subproc'):
    if authorID == 873212295684173904:
      return_code = subprocess.check_output(userMsg[9:], shell=True)
      await message.channel.send(f"```{return_code.decode('UTF-8')}```")
    else:
      await message.channel.send('```operation not permitted```')

  # run python
  if userMsg.startswith('!evala'):
    if authorID == 873212295684173904:
       await message.channel.send('```'+str(eval(userMsg[6:]))+'```')

  # eval
  if userMsg.startswith('!eval'):
    # print(eval(userMsg), eval(userMsg[5:]))
    # print(any(c.isalpha() for c in userMsg[5:]))
    if not any(c.isalpha() for c in userMsg[5:]):
      await message.channel.send('```'+str(eval(userMsg[5:]))+'```')
    else:
      await message.channel.send('```operation not permitted```')
    
  


  # triggers
  if userMsg.lower() in triggerKeys:
    await message.channel.send(autoresponderData[userMsg])
  if listenTrig and homeworkID == authorID:
    await message.channel.send(
        f'added key value pair `{valueTrig}` and `{userMsgFormatted}`')
    autoresponderData[valueTrig] = userMsgFormatted
    sheet.update_cell(2, 1, str(autoresponderData))
    listenTrig = False
  if userMsg.startswith('!addtrig'):
    print(userMsgTrigger, userMsgTrigger[8:])
    if userMsgTrigger[8:].lower() in ['enterthegungeon', 'bestgame']:
      await message.channel.send(f'`stop it tyler... STOP`')
    elif userMsg[9:] in triggerKeys:
      await message.channel.send(
          f'`this trigger is already add it, either override it or delete it`')
    else:
      await message.channel.send(f'what should i respond to `{userMsg[9:]}`?')
      valueTrig = userMsg[9:]
      homeworkID = authorID
      listenTrig = True
  if userMsg.startswith('!listtrig'):
    if not autoresponderData:
      await message.channel.send(
          'theres currently no triggers set, use !addtrig to add some!')
    else:
      await message.channel.send(autoresponderData)
  if userMsg.startswith('!deltrig') and userMsg in triggerKeys:
    if authorID != 873212295684173904:
      await message.channel.send(
          '`you dont have the permissions to run this command`')
    else:
      del autoresponderData[userMsg[9:]]
      sheet.update_cell(2, 1, str(autoresponderData))
  if userMsg.startswith('!deltrig max'):
    if authorID != 873212295684173904:
      await message.channel.send(
          '`you dont have the permissions to run this command`')
    else:
      autoresponderData = {}
      sheet.update_cell(2, 1, str(autoresponderData))


client.run(TOKEN)
