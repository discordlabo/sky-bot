'''
Discord Bot "Sky Bot"
Core
core/core.py
WIP'''
__version__ = '0.4.27 Dev Build 41'
import secrets,data,status
import requests,fuckit
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
x=open('status.py','w')
x.write('running=1\nid=\'{}\''.format(status.id))
x.close()
y=open('pkg.csv')
z=y.read()
y.close()

app = discord.Client()
bot = commands.Bot(command_prefix='')

for i in z.split(','):
  fuckit(i.replace('\n',''))
  pkg_io = []
  print('i Init [{}]'.format(i.replace('\n','')))
  try:
    eval('pkg_io.append(['+i.replace('\n','')+'.io(__version__,bot),'+i.replace('\n','')+'.io(__version__,bot).name()])')
  except Exception as error:
    print('|- Failed to start {} - {}'.format(i.replace('\n',''),error))
y.close()

@bot.event
@asyncio.coroutine
def on_ready():
  print('i Bot Ready')

@bot.event
@asyncio.coroutine
def on_message(message):
  y=open('pkg.csv')
  z=y.read()
  y.close()
  if message.content.startswith(':'):
    if len(message.content) == 1:
      yield from bot.send_message(message.channel,'This is the Development Prefix. Use it only if you know what you are doing! (ID = {})'.format(secrets.id))
    elif message.content == ':about':
      yield from bot.send_message(message.channel,'''@Sky#2509-{} {} by @python3lover#4401 and @__toad_#3754 running on Ubuntu.
Packages Installed:
{}
Libraries in Use:
* requests (python-requests)
* discord (discord.py)
* asyncio (built-in)'''.format(status.id,__version__,'* '+z.replace(',','\n* ').replace('sky-','')))
    elif message.content == ':halt':
      yield from bot.send_message(message.channel,':octagonal_sign: Bye...')
      x=open('status.py','w')
      x.write('running=0\nid=\'{}\''.format(status.id))
      x.close()
      exit()
    elif message.content.startswith(':http/'):
#       if message.content.startswith(':http/get/'):
#         yield from bot.send_message(message.channel,requests.get((message.content+' ')[10:-1]).text)
      yield from bot.send_message(message.channel,'HTTP(S) Mode is not yet supported.')
    elif message.content == ':rehalt':
      yield from bot.send_message(message.channel,':octagonal_sign: ReHalt is not yet supported.')
    elif message.content.startswith(':add/'):
      pkgName = message.content.split('/')[-1]
      if pkgName in (',' + z.replace('\n','')).replace(',',',sky_').split(','):
        yield from bot.send_message(message.channel,':arrow_down: Updating package {}...'.format(pkgName))
        r = requests.get('https://raw.githubusercontent.com/discordlabo/sky-pkg/master/{}/core.py'.format(pkgName))
        if str(r.status_code)[0] in ['1','2']:
          file = open('sky_'+pkgName+'.py','w')
          file.write(r.text)
          file.close()
          yield from bot.send_message(message.channel,':arrow_down: Updated package {}.'.format(pkgName))
        else:
          yield from bot.send_message(message.channel,':warning: Failed to add package {}, {}, {}'.format(pkgName,r.status_code,r.text))
      else:
        yield from bot.send_message(message.channel,':arrow_down: Adding package {}...'.format(pkgName))
        r = requests.get('https://raw.githubusercontent.com/discordlabo/sky-pkg/master/{}/core.py'.format(pkgName))
        if str(r.status_code)[0] in ['1','2']:
          file = open('sky_'+pkgName+'.py','w')
          file.write(r.text)
          file.close()
          file = open('pkg.csv','a')
          file.write(',sky_'+pkgName)
          file.close()
          yield from bot.send_message(message.channel,':arrow_down: Added package {}.'.format(pkgName))
        else:
          yield from bot.send_message(message.channel,':warning: Failed to add package {}, {}, {}.'.format(pkgName,r.status_code,r.text))
    else:
      pass
  elif message.content.startswith('s!'):
    if message.content == 's!about':
      yield from bot.send_message(message.channel,'@Sky {} by @python3lover#4401 and @__toad_#????'.format(__version__))
    elif message.content.startswith('s!calc/'):
      try:
        ans = eval((message.content+' ')[6:-1])
      except SyntaxError:
        ans = ':octagonal_sign: Syntax Error'
      except ZeroDivisionError:
        ans = 'Infinity'
      except:
        ans = ':octagonal_sign: Unexpected Error'
      yield from bot.send_message(message.channel,ans)
    else:
      yield from bot.send_message(message.channel,'Hi! I\'m Sky, a bot.')
  elif message.content in data.badWords:
    yield from bot.delete_message(message)
  else:
    for i in pkg_io:
      i[0].call(message)

bot.run(secrets.token)
x=open('status.py','w')
x.write('running=0\nid=\'{}\''.format(status.id))
x.close()
