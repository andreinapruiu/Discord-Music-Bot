#Discord bot made in python(simple with just a few functions)
#Copyright (C) 2021 Andrei Napruiu
#Copyright (C) 2021 IDST LAB 03 - Python Discord Bot
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#!./.venv/bin/python
 
import argparse
import discord      # base discord module
import code         # code.interact
import os           # environment variables
import inspect      # call stack inspection
import random       # dumb random number generator 

from os import listdir              #functii care vor ajuta la comanda !list
from os.path import isfile, join
from discord import message

from discord.ext import commands    # Bot class and utils
 
################################################################################
############################### HELPER FUNCTIONS ###############################
################################################################################
 
# log_msg - fancy print
#   @msg   : string to print
#   @level : log level from {'debug', 'info', 'warning', 'error'}
def log_msg(msg: str, level: str):
    # user selectable display config (prompt symbol, color)
    dsp_sel = {
        'debug'   : ('\033[34m', '-'),
        'info'    : ('\033[32m', '*'),
        'warning' : ('\033[33m', '?'),
        'error'   : ('\033[31m', '!'),
    }
 
    # internal ansi codes
    _extra_ansi = {
        'critical' : '\033[35m',
        'bold'     : '\033[1m',
        'unbold'   : '\033[2m',
        'clear'    : '\033[0m',
    }
 
    # get information about call site
    caller = inspect.stack()[1]
 
    # input sanity check
    if level not in dsp_sel:
        print('%s%s[@] %s:%d %sBad log level: "%s"%s' % \
            (_extra_ansi['critical'], _extra_ansi['bold'],
             caller.function, caller.lineno,
             _extra_ansi['unbold'], level, _extra_ansi['clear']))
        return
 
    # print the damn message already
    print('%s%s[%s] %s:%d %s%s%s' % \
        (_extra_ansi['bold'], *dsp_sel[level],
         caller.function, caller.lineno,
         _extra_ansi['unbold'], msg, _extra_ansi['clear']))
 
parser = argparse.ArgumentParser()
parser.add_argument("log_msg", token=log_msg('save your token in the BOT_TOKEN env variable!', 'error'))
################################################################################
############################## BOT IMPLEMENTATION ##############################
################################################################################
 
# bot instantiation
bot = commands.Bot(command_prefix='!')
 
# on_ready - called after connection to server is established
@bot.event
async def on_ready():
    log_msg('logged on as <%s>' % bot.user, 'info')
 
# on_message - called when a new message is posted to the server
#   @msg : discord.message.Message
@bot.event
async def on_message(msg):
    # filter out our own messages
    if msg.author == bot.user:
        return
 
    log_msg('message from <%s>: "%s"' % (msg.author, msg.content), 'debug')
 
    # overriding the default on_message handler blocks commands from executing
    # manually call the bot's command processor on given message
    await bot.process_commands(msg)


# on_voice_state_update - daca nu mai e nimeni pe canalul de voce, deconecteaza botul imediat
@bot.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        # iese automat din executie daca botul nu e conectat la voice channel
        return 

    if len(voice_state.channel.members) == 1:
        await voice_state.disconnect()



# roll - rng chat command
#   @ctx     : command invocation context
#   @max_val : upper bound for number generation (must be at least 1)
@bot.command(brief='Generate random number between 1 and <arg>')
async def roll(ctx, max_val: int):
    # argument sanity check
    if max_val < 1:
        raise Exception('argument <max_val> must be at least 1')
 
    await ctx.send(random.randint(1, max_val))
 
# roll_error - error handler for the <roll> command
#   @ctx     : command that crashed invocation context
#   @error   : ...
@roll.error
async def roll_error(ctx, error):
    await ctx.send(str(error))




@bot.command(brief='Join channel')
async def join(ctx):

    #verific daca e cineva in voice channelul din care s-a dat comanda
    if ctx.author.voice is None:
        raise Exception(f'{ctx.author} is not in a voice channel =(')

    voice_channel = ctx.author.voice.channel

    #conectez bot-ul
    if ctx.voice_client is None:
        await voice_channel.connect()

    await ctx.send(f'Salut! Am intrat pe canalul de voce {voice_channel}!')

@join.error
async def join_error(ctx, error):
    await ctx.send(str(error))



@bot.command(brief='Joins channel and plays the selected mp3 channel')
async def play(ctx, song: str):

    #verific daca e cineva in voice channelul din care s-a dat comanda
    if ctx.author.voice is None:
        raise Exception(f'{ctx.author} is not in a voice channel =(')

    voice_channel = ctx.author.voice.channel

    #conectez bot-ul
    if ctx.voice_client is None:
        await voice_channel.connect()
        await ctx.send(f'Salut! Am intrat pe canalul de voce {voice_channel}!')

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    #da play la melodia ceruta, daca exista
    music = song+".mp3"

    if os.path.exists("/home/student/lab03_python(discord)/muzica/"+music):
        voice.play(discord.FFmpegPCMAudio("/home/student/lab03_python(discord)/muzica/"+music))
    else:
        await ctx.send("Nu am gasit melodia in folderul tau de muzica... sorry=(")


@play.error
async def play_error(ctx, error):
    await ctx.send(str(error))




@bot.command(brief='Stops the music')
async def pause(ctx):

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Nu am ce sa opresc!")

@pause.error
async def pause_error(ctx, error):
    await ctx.send(str(error))



@bot.command(brief='Stops the music')
async def resume(ctx):

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
    else:
        await ctx.send("Nu am ce sa opresc!")

@resume.error
async def resume_error(ctx, error):
    await ctx.send(str(error))




@bot.command(brief='Lists all the mp3 files from the directory of music')
async def list(ctx):

    #afiseaza toate fisierele mp3 din folderul in care ar trebui sa se afle muzica
    path = "/home/student/lab03_python(discord)/muzica" #aici se mentioneaza calea in care se afla muzica
    fisiere = os.listdir(path) #functia care gaseste toate fisierele din folder

    await ctx.send(fisiere)

@list.error
async def list_error(ctx, error):
    await ctx.send(str(error))





@bot.command(brief='Leave voice channel')
async def scram(ctx):

    #verific daca e cineva in voice channel
    if ctx.author.voice is None:
        raise Exception(f'{ctx.author} is not in a voice channel =(')

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    voice_channel = ctx.author.voice.channel

    #daca a fost in voice channel, dar bot-ul nu e conectat, apare eroare
    if ctx.voice_client is None:
        raise Exception('Nu sunt conectat. Nu ma poti da afara XP')
    
    #deconectez bot-ul daca este conectat, il dau afara
    if voice.is_connected():
        await voice.disconnect()

    #mesaj de adio!
    await ctx.send(f'Salut! Am iesit de pe canalul de voce {voice_channel}!')

@scram.error
async def scram_error(ctx, error):
    await ctx.send(str(error))


@bot.command(brief='Greetings!')
async def hello(ctx, name: str):
    #mic mesaj de salut
    await ctx.send('Multe salutari si sunt incantat de cunostinta, '+name+'!')

@hello.error
async def hello_error(ctx, error):
    await ctx.send(str(error))




@bot.command(brief='Show all commands')
async def helpme(ctx):

    await ctx.send('!play <song> - Intra pe canal si da play la melodia song.mp3 salvata in locatia specificata in cod')
    await ctx.send('!list - afiseaza toate melodiile existente la locatia specificata in cod')
    await ctx.send('!roll <nr> - afiseaza un numar random intre 1 si nr')
    await ctx.send('!pause - opreste melodia curenta')
    await ctx.send('!resume - reporneste melodia curenta')
    await ctx.send('!scram - da afara botul de pe canalul de voce')
    await ctx.send('!join - adauga botul in canalul de voce in care s-a dat comanda')
    await ctx.send('!hello <nume> - face botul sa salute pe oricine cu numele de <nume>')

@helpme.error
async def helpme_error(ctx, error):
    await ctx.send(str(error))

################################################################################
############################# PROGRAM ENTRY POINT ##############################
################################################################################
 
if __name__ == '__main__':
    # check that token exists in environment
    if 'BOT_TOKEN' not in os.environ:
        log_msg('save your token in the BOT_TOKEN env variable!', 'error')
        exit(-1)
    # launch bot (blocking operation)
    bot.run(os.environ['BOT_TOKEN'])
