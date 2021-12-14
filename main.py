import discord
import tracemoepy
import random
import youtube_dl
import asyncio
import os
import json
import requests
from discord.ext import commands
from commands.searchAnime import animeSearch
from commands.searchManga import mangaSearch
from commands.searchStudio import studioSearch
from commands.searchCharacter import charSearch
from keep_alive import keep_alive

tracemoe = tracemoepy.tracemoe.TraceMoe()

client = commands.Bot(command_prefix=["@", '/', '!', '$', '.', '?'])

token = "Nzk2NzIzOTk5NDM4NDA1NjUy.X_cFCw.Dml9QOX2usPVypMI72CMXHGNqwo"
api_key = "your_openweathermap_api_key"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

client.remove_command('help')


#Bot Ready
@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game("Type @help"))
    print(f'{client.user} has connected to Discord!')


#Welcome And Leave
@client.event
async def on_member_join(member):
    print("Welcome to YouthFox, enjoy your stay :)" + member.name)
    await client.send_message(member, newUserDMMessage)
    await client.send_message(discord.Object(id='733668902302646335'),
                              'Welcome!')
    print("Sent message to " + member.name)
    print("Sent message about " + member.name + " to #Welcome")


@client.event
async def on_member_remove(member):
    print("Hopefully you come back to YouthFox" + member.name +
          "See you soon Buddy!😭")
    await client.send_message(discord.Object(id='799264975361277953'),
                              member.name + ' left')
    print("Sent message to #see-you-soon")


#Embedded Help Centre
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(title="Help from BOT",
                          description="Useful commands with it's function.")
    embed.set_author(name='Command_prefix=[@ , /, $ , ! , . , ? ]')
    embed.add_field(name="anime",
                    value="Search your favourite anime.",
                    inline=False)
    embed.add_field(name="character",
                    value="Search the favourite anime waifus or husbandos.",
                    inline=False)
    embed.add_field(name="clear",
                    value="Clears or delete the message.",
                    inline=False)
    embed.add_field(name="credits",
                    value="This command returns the credits.",
                    inline=False)
    embed.add_field(name="die",
                    value="This command returns a random last words.",
                    inline=False)
    embed.add_field(name="eight_ball",
                    value="Answers from the beyond.",
                    inline=False)
    embed.add_field(name="join",
                    value="This command makes the bot join the voice channel.",
                    inline=False)
    embed.add_field(
        name="leave",
        value="This command makes the bot leaves the voice channel.",
        inline=False)
    embed.add_field(name="manga", value="Search your favourite manga.")
    embed.add_field(name="pause",
                    value="This command makes the bot pause the music.",
                    inline=False)
    embed.add_field(
        name="ping",
        value="Prints pong back to the channel with latency of your network.",
        inline=False)
    embed.add_field(
        name="play",
        value="This command makes the bot play the music using youtube url.",
        inline=False)
    embed.add_field(name="queue",
                    value="This command adds a song to the queue.",
                    inline=False)
    embed.add_field(name="remove",
                    value="This command removes an item from the list.",
                    inline=False)
    embed.add_field(name="resume",
                    value="This command makes the bot resume the music.",
                    inline=False)
    embed.add_field(name="server_info", value="Display server", inline=False)
    embed.add_field(name="stop",
                    value="This command makes the bot stop the music.",
                    inline=False)
    embed.add_field(name="studio",
                    value="Search your favourite anime production company.",
                    inline=False)
    embed.add_field(name="tictactoe",
                    value="Play tic-tac-toe game with your friends",
                    inline=False)
    embed.add_field(name="weather",
                    value="Display weather of desired city",
                    inline=False)
    await ctx.send(embed=embed)


#Commands Centre
@client.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong with {round(client.latency* 1000)}ms')


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=3):
    await ctx.channel.purge(limit=amount)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please pass in all required arguments :rolling_eyes:.")
    if isinstance(error, commands.CommandNotFound):
        print("Command not found :angry:.")
    else:
        print(error)


@client.command(
    aliases=["ANIME", "a"], )
async def anime(ctx, *, title):
    embed = animeSearch(title)
    await ctx.send(embed=embed)


@client.command(aliases=["MANGA", "m"])
async def manga(ctx, *, title):
    embed = mangaSearch(title)
    await ctx.send(embed=embed)


@client.command(aliases=['STUDIO', 's'])
async def studio(ctx, *, studioName):
    embed = studioSearch(studioName)
    await ctx.send(embed=embed)


@client.command(aliases=["CHARACTER", 'ch', 'char'])
async def character(ctx, *, charName):
    embed = charSearch(charName)
    await ctx.send(embed=embed)


@client.command(name='8ball',
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        "As I see it, yes", "Yes", "No", "Very likely", "Not even close",
        "Maybe", "Very unlikely", "Gino's mom told me yes",
        "Gino's mom told me no", "Ask again later", "Better not tell you now",
        "Concentrate and ask again", "Don't count on it", " It is certain",
        "My sources say no", "Outlook good", "You may rely on it",
        "Very Doubtful", "Without a doubt"
    ]
    await context.send(
        random.choice(possible_responses) + ", " +
        context.message.author.mention)


@client.command()
async def credit(ctx):
    await ctx.send('Made by `Takeru`')
    await ctx.send('Thanks to `Sid and Gati` for coming up with the idea')
    await ctx.send(
        'Thanks to `Sam` for helping with the `die` and `credit` command')


@client.command()
async def die(ctx):
    responses = [
        'why have you brought my short life to an end',
        'i could have done so much more', 'i have a family, kill them instead'
    ]
    await ctx.send(random.choice(responses))


#Youtube Music Player
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address':
    '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options),
                   data=data)


@client.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()


@client.command()
async def queue_(ctx, url):
    global queue

    queue.append(url)
    await ctx.send(f'`{url}` added to queue!')


@client.command()
async def remove(ctx, number):
    global queue

    try:
        del (queue[int(number)])
        await ctx.send(f'Your queue is now `{queue}!`')

    except:
        await ctx.send(
            'Your queue is either **empty** or the index is **out of range**')


@client.command()
async def play(ctx, url):

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(player,
                           after=lambda e: print('Player error: %s' % e)
                           if e else None)

    await ctx.play()


@client.command()
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()


@client.command()
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()


@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@client.command()
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.stop()


#TIC-TAC-TOE
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7],
                     [2, 5, 8], [0, 4, 8], [2, 4, 6]]


@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:"
        ]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send(
            "A game is already in progress! Finish it before starting a new one."
        )


@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(+ " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send(
                    "Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile."
                )
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[
                condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "Please make sure to mention/ping players (ie. <@688534433879556134>)."
        )


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


#Server Info
@client.command()
async def server_info(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(title=name + " Server Information",
                          description=description,
                          color=discord.Color.blue())
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)
    await ctx.send(embed=embed)


#Weather
@client.command()
async def weather(ctx, *, city: str):
    city_name = city
    complete_url= base_url + "appid=" + api_key + '&q=' + city_name 
    response = requests.get(complete_url)
    x = response.json()
    channel = ctx.message.channel

    if x["cod"] != "404":
        async with channel.typing():
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsiuis = str(
                round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            weather_description = z[0]["description"]
            embed = discord.Embed(
                title=f"Weather in {city_name}",
                color=ctx.guild.me.top_role.color,
                timestamp=ctx.message.created_at,
            )
            embed.add_field(name="Descripition",
                            value=f"**{weather_description}**",
                            inline=False)
            embed.add_field(name="Temperature(C)",
                            value=f"**{current_temperature_celsiuis}°C**",
                            inline=False)
            embed.add_field(name="Humidity(%)",
                            value=f"**{current_humidity}%**",
                            inline=False)
            embed.add_field(name="Atmospheric Pressure(hPa)",
                            value=f"**{current_pressure}hPa**",
                            inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}")

        await channel.send(embed=embed)
    else:
        await channel.send("City not found.")


keep_alive()

client.run(token)
