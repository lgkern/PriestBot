import discord
from discord import Forbidden
from discord.ext import commands
import random
from dict import DictionaryReader
from botkey import Key
from subprocess import call
import sys
import logging

logging.basicConfig(level=logging.INFO)

description = '''I'm PriestBot, your robot friend for links and quick info!

Below you'll find my basic commands.

You can find my full list of commands at https://github.com/lgkern/discord.py/blob/async/examples/dictEntries.txt'''
bot = commands.Bot(command_prefix='!', description=description)

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
	if message.author == client.user:
		return
	if message.content.startswith('!'):
		if message.content.startswith('!fullupdate'):
			call(["git","pull"])
			call(["cmdhere.bat"])
			sys.exit()
		elif message.content.startswith('!update'):
			call(["git","pull"])
		elif message.content.startswith('!send'):
			p = DictionaryReader()
			roles = message.author.roles
			canSend = False
			for role in roles:
				canSend = canSend or (role.name in p.roles())
			if not canSend:
				print('{0.author.name} can\'t send whispers'.format(message))
				return
			entries = message.content.split(' ')
			target = message.mentions[0]
			if target != None:
				entry = ' '.join(entries[2::])
				msg = p.commandReader(entry)
				if msg != None:
					await client.send_message(target, msg)
					try:
						client.delete_message(message)	
					except Exception:
						client.send_message(message.channel, 'Can\'t delete shi... stuff here')
					await client.send_message(message.author, 'Message sent to {0.mention}'.format(target))
				else:
					await client.send_message(message.channel, 'Invalid Message, {0.mention}'.format(message.author))
		elif message.content.startswith('!item'):
			p = DictionaryReader()
			msg = p.itemReader(message.content[1::])
			await client.send_message(message.channel, msg)
		else:
			command = message.content[1::].split(' ')[0]
			p = DictionaryReader()
			msg = p.commandReader(message.content[1::])
			if msg != None:
				if command in p.whisperCommands():
					await client.send_message(message.author, msg)
					client.delete_message(message)
				else:
					await client.send_message(message.channel, msg)
			#msg = 'Hello {0.author.mention}'.format(message)

client.run(Key().value())
#bot.run(Key().value())

