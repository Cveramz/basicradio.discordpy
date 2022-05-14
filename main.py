import discord
from discord import FFmpegPCMAudio
from discord.ext import commands, tasks
from discord.utils import get
from discord import Embed
from random import choice
from discord.ext.commands import Cog
from discord.ext.commands import has_permissions
from dotenv import load_dotenv
from server import keep_alive
import asyncio
import youtube_dl
import mad
import random
from gtts import gTTS
import soundfile as sf
import calendar

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot('-', intents=intents)

load_dotenv()
bot = commands.Bot(command_prefix = "-", description="MENÚ DE AYUDA:D")

# Suppress noise about console usage from errors
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
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}


queue = {}
def addToQueue(guild, song):
    if guild.id in queue:
        queue[guild.id] = []
    queue[guild.id].append(song)

async def playSong(ctx, channel):
    async with ctx.typing():
        song = queue[channel.guild.id].pop(0, None)
        if song == None:
            return
        player = await YTDLSource.from_url(song, loop=bot.loop, stream=True)
        channel.play(
            player,
            after=lambda e:
             playSong(ctx, channel)
        )

    await ctx.send('**Now playing:** {}'.format(player.title))

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
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Comando para testeo manual"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()


    


    @commands.command()
    async def play(self, ctx, *, url):
        """Reproduce musica, ingresa un video a buscar en youtube o ingresa un url"""
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"Groovy", description=f'Ahora sonando: {player.title}', color=discord.Color.blue() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/VvY0hVFH/youtube-logo-gif.gif")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" yt")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")
      
      
    @commands.command()
    async def p(self, ctx, *, url):
        """Reproduce musica, ingresa un video a buscar en youtube o ingresa un url"""
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"Groovy", description=f'Ahora sonando: {player.title}', color=discord.Color.blue() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/VvY0hVFH/youtube-logo-gif.gif")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" yt")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")
      
    
      
    @commands.command()
    async def radio_disney(self, ctx, *, url: str = 'https://unlimited3-cl.dps.live/disney/mp364k/icecast.audio'):
        """Reproduce la radio DISNEY de Chile"""
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"Groovy", description=f'Ahora sonando: Radio Disney\nObserva más radios con ***-radio***\n\nCambia el volumen con ***-volumen [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.blue() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/qvmVqZh8/radio-disney.gif")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" stream")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")
    @commands.command()
    async def radio_ilovemusic(self, ctx, *, url: str = 'https://streams.ilovemusic.de/iloveradio1.mp3'):
        """Reproduce una radio alemana con buena musica"""
        
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"Groovy", description=f'Ahora sonando: I LOVE MUSIC [Deutsch]\nObserva más radios con ***-radio***\n\nCambia el volumen con ***-volumen [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.red() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/1Xc6rFDZ/f4c5e12a-387e-4041-a5d9-d41e68343870.png")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" stream")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")
    
    @commands.command()
    async def radio_chill(self, ctx, *, url: str = 'https://streams.ilovemusic.de/iloveradio17.mp3'):
        """Reproduce musica chill"""
        
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"Groovy", description=f'Ahora sonando: I LOVE MUSIC [Deutsch]: Chill Music\nObserva más radios con ***-radio***\n\nCambia el volumen con ***-volumen [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.red() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/1Xc6rFDZ/f4c5e12a-387e-4041-a5d9-d41e68343870.png")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" stream")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")

    @commands.command()
    async def radio_hard(self, ctx, *, url: str = 'https://streams.ilovemusic.de/iloveradio21.mp3'):
        """Reproduce musica del genero HardStyle"""
        
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"Groovy", description=f'Ahora sonando: I LOVE MUSIC [Deutsch]: *HARD STYLE*\nObserva más radios con ***-radio***\n\nCambia el volumen con ***-volumen [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.red() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/VshdSz2k/tumblr-mgeu6fl-Zh-V1rd7d9oo1-1280.gif")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" stream")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")


    @commands.command()
    async def radio_monstercat(self, ctx, *, url: str = 'https://streams.ilovemusic.de/iloveradio24.mp3'):
        """Escucha musica de monstercat"""
        
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"Groovy", description=f'Ahora sonando: I LOVE MUSIC [Deutsch]: *MONSTERCAT*\nObserva más radios con ***-radio***\n\nCambia el volumen con ***-volumen [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.red() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/T2bcfNxt/monstercat.gif")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" stream")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")

    @commands.command()
    async def radio_party(self, ctx, *, url: str = 'https://streams.ilovemusic.de/iloveradio14.mp3'):
        """Reproduce musica piolita xd"""
        
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"Groovy", description=f'Ahora sonando: I LOVE MUSIC [Deutsch]: *Party Time*\nObserva más radios con ***-radio***\n\nCambia el volumen con ***volumen [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.red() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/J7jj9y3g/tenor.gif")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" stream")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")
    @commands.command()
    async def radio_carolina(self, ctx, *, url: str = 'http://unlimited3-cl.dps.live/carolinafm/aac/icecast.audio'):
        """Reproduce la radio Carolina de Chile"""
        
        try:
          async with ctx.typing():
              await ctx.reply("Cargando. . . . ",mention_author=True)
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print(f'Error de reproducción: {e}') if e else None)
          embed = discord.Embed(title=f"Groovy", description=f'Ahora sonando: I LOVE MUSIC [Deutsch]: *Party Time*\nObserva más radios con ***-radio***\n\nCambia el volumen con ***-volumen [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.red() )
          embed.set_thumbnail(url=f"https://i.postimg.cc/J7jj9y3g/tenor.gif")
          await ctx.reply(embed=embed, mention_author=True)
          print(ctx.guild.name+" stream")
        except:
          await ctx.send("Error con el enlace o error para conectar al canal. Contactar a @cvr#2378")

    @commands.command()
    async def volumen(self, ctx, volume: int):
        """Cambiar el volumen [0-100]"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Desconecta el bot del canal de audio"""
        embed = discord.Embed(title=f"Groovy", description=f'La reproducción se ha detenido\nObserva más radios con ***-radio***\n\nCambia el volumen con ***-volumen [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.blue() )
        embed.set_thumbnail(url=f"https://i.postimg.cc/85mbkxsG/Stop-button-play-pause-music.png")
        await ctx.reply(embed=embed, mention_author=True)
        print(ctx.guild.name+" stop")
        await ctx.voice_client.disconnect()

    @commands.command()
    async def leave(self, ctx):
        """Desconecta el bot del canal de audio"""
        embed = discord.Embed(title=f"Groovy", description=f'La reproducción se ha detenido\nObserva más radios con ***-radio***\n\nCambia el volumen con ***-volumen [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.blue() )
        embed.set_thumbnail(url=f"https://i.postimg.cc/85mbkxsG/Stop-button-play-pause-music.png")
        await ctx.reply(embed=embed, mention_author=True)
        print(ctx.guild.name+" stop")
        await ctx.voice_client.disconnect()

    @commands.command()
    async def salir(self, ctx):
        """Desconecta el bot del canal de audio"""
        embed = discord.Embed(title=f"Groovy", description=f'La reproducción se ha detenido\nObserva más radios con ***-radio***\n\nCambia el volumen con ***-volumen [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.blue() )
        embed.set_thumbnail(url=f"https://i.postimg.cc/85mbkxsG/Stop-button-play-pause-music.png")
        await ctx.reply(embed=embed, mention_author=True)
        print(ctx.guild.name+" stop")
        await ctx.voice_client.disconnect()

    @commands.command()
    async def desconectar(self, ctx):
        """Desconecta el bot del canal de audio"""
        embed = discord.Embed(title=f"Groovy", description=f'La reproducción se ha detenido\nObserva más radios con ***-radio***\n\nCambia el volumen con ***-volumen [x]*** (X puede ser un numero de 0 a 100)', color=discord.Color.blue() )
        embed.set_thumbnail(url=f"https://i.postimg.cc/85mbkxsG/Stop-button-play-pause-music.png")
        await ctx.reply(embed=embed, mention_author=True)
        print(ctx.guild.name+" stop")
        await ctx.voice_client.disconnect()

    @play.before_invoke
    @p.before_invoke
    @radio_disney.before_invoke
    @radio_ilovemusic.before_invoke
    @radio_chill.before_invoke
    @radio_hard.before_invoke
    @radio_monstercat.before_invoke
    @radio_party.before_invoke
    @radio_carolina.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()





@bot.command()
async def ayuda(ctx):
    embed = discord.Embed(title=f"Listado Comandos", description="wena, soy un intento de Groovy, no me acuerdo como era esta wa xD.\nComandos:\n-play (nombre de canción o link)\n-radios\n-donate\n-avatar (@usuario)\n-chao", color=discord.Color.red() )
    embed.set_thumbnail(url=f"https://i.postimg.cc/XYcsJQBb/icon-512x512-321737.png")
    await ctx.send(embed=embed)
    print(ctx.guild.name+ " Help")


@bot.command()
async def donate(ctx):
    """Link para donaciones"""
    embed = discord.Embed(title=f"HAZ CLICK AQUÍ PARA AYUDARME", description="Hola!\n Te agradecería si me hechas una ayuda economica vía paypal\n Haz click en en el titulo :D", url= "https://paypal.me/cfvraccount" , color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://i.postimg.cc/GpVvGZYT/Whats-App-Image-2021-04-21-at-15-27-06.jpg")
    await ctx.send(embed=embed)
    print(ctx.guild.name+ " Donate")

"""@bot.command()
async def links(ctx):
  OBTENER LISTADO LINKS
  embed=discord.Embed(title="HAZ CLICK AQUÍ PARA ACCEDER A LOS LINKS", url="https://linktr.ee/cvrdev", description="Aquí puedes encontrar el link del drive con la información de las transferencias y también enlaces para transferir vía paypal y mach.", color=0x7d04f6)
  embed.set_thumbnail(url=f"https://static.wixstatic.com/media/889949_4beaae02fa714eb2b55bdbbf0e1ad0ac~mv2.png/v1/fill/w_362,h_358,al_c,q_85,usm_0.66_1.00_0.01/889949_4beaae02fa714eb2b55bdbbf0e1ad0ac~mv2.webp")
  await ctx.send(embed=embed)
"""
@bot.command()
async def radios(ctx):
    """Listado de radios"""
    embed = discord.Embed(title=f"OPAAA RADIOS DISPONIBLES", description="-radio_disney\n-radio_ilovemusic\n-radio_chill\n-radio_hard\n-radio-monstercat\n-radio_party\n***Apagar con `-stop`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://i.postimg.cc/XYcsJQBb/icon-512x512-321737.png")
    await ctx.send(embed=embed)
    print(ctx.guild.name+ "Lista radio")

@bot.command()
async def avatar(ctx, member:discord.Member):
  """Obten el la imagen de algún usuario"""
  await ctx.send(member.avatar_url)

@bot.command()
async def adios(ctx):
  embed = discord.Embed(title="adioss", color=discord.Color.purple())
  embed.set_image(url="https://i.postimg.cc/DZbN6J3J/54c7cdd0dac608e45fd4a4eef9fb7aa6.gif")
  await ctx.channel.send(embed=embed)
@bot.command()
async def chao(ctx):
  embed = discord.Embed(title="Xiaonovimo¡", color=discord.Color.purple())
  embed.set_image(url="https://i.postimg.cc/Ss8Z8Bcc/tenor.gif")
  await ctx.channel.send(embed=embed)

@bot.command()
async def amsiedad(ctx):
  embed = discord.Embed(title="Xiaonovimo¡", color=discord.Color.purple())
  embed.set_image(url="https://i.postimg.cc/ZnzCQFbf/amsiedad-1.gif")
  await ctx.channel.send(embed=embed)

@bot.command()
async def ansiedad(ctx):
  embed = discord.Embed(title="Xiaonovimo¡", color=discord.Color.purple())
  embed.set_image(url="https://i.postimg.cc/ZnzCQFbf/amsiedad-1.gif")
  await ctx.channel.send(embed=embed)

@bot.command()
async def bye(ctx):
  embed = discord.Embed(title="Xiaonovimo¡", color=discord.Color.purple())
  embed.set_image(url="https://i.postimg.cc/Prtq8qP8/bye-bye-bye.gif")
  await ctx.channel.send(embed=embed)


@bot.command()
async def borrar(ctx, amount=2):
  await ctx.channel.purge(limit=amount)
  print(ctx.guild.name+ "Borrar")


@bot.command()
async def purge(ctx, amount):
  amount = int (amount)
  await ctx.channel.purge(limit=amount)
  print(ctx.guild.name+ "Purga")

@bot.command(pass_context=True)
async def d(ctx, tiempo, *,texto, amount=1):
    dat=random.randint(1,999999999)
    dat=str(dat)
    audio=("ejemplo"+dat+".mp3")
    language="es"
    sp=gTTS(text=texto, lang = language,slow=False)
    sp.save(audio)
    #time.sleep(1)

    if (ctx.author.voice):
      channel=ctx.message.author.voice.channel
      await channel.connect()
      source=FFmpegPCMAudio("ejemplo"+dat+".mp3")
      ctx.voice_client.play(source)
      await asyncio.sleep(1)
    await ctx.channel.purge(limit=amount)
    tiempo=int (tiempo)
    await asyncio.sleep(tiempo)
    await ctx.voice_client.disconnect()
@bot.command(pass_context=True)
async def den(ctx,tiempo, *,texto):
    dat=random.randint(1,999999999)
    dat=str(dat)
    audio=("ejemplo"+dat+".mp3")
    language="en"
    sp=gTTS(text=texto, lang = language,slow=False)
    sp.save(audio)
    #time.sleep(1)

    if (ctx.author.voice):
      channel=ctx.message.author.voice.channel
      await channel.connect()
      source=FFmpegPCMAudio("ejemplo"+dat+".mp3")
      ctx.voice_client.play(source)
      await asyncio.sleep(1)
    tiempo=int (tiempo)
    await asyncio.sleep(tiempo)
    await ctx.voice_client.disconnect()
@bot.command(pass_context=True)
async def dbr(ctx,tiempo, *,texto):
    dat=random.randint(1,999999999)
    dat=str(dat)
    audio=("ejemplo"+dat+".mp3")
    language="pt"
    sp=gTTS(text=texto, lang = language,slow=False)
    sp.save(audio)
    #time.sleep(1)

    if (ctx.author.voice):
      channel=ctx.message.author.voice.channel
      await channel.connect()
      source=FFmpegPCMAudio("ejemplo"+dat+".mp3")
      ctx.voice_client.play(source)
      await asyncio.sleep(1)
    tiempo=int (tiempo)
    await asyncio.sleep(tiempo)
    await ctx.voice_client.disconnect()

@bot.command(help='This command plays music')
async def reproducir(ctx, url):
        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel")
            return

        else:
            channel = ctx.message.author.voice.channel
        
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if channel != voice and voice is None:
            await channel.connect()
        elif channel != voice and voice is not None:
            await ctx.send("Already connected to a channel")
            return

        server = ctx.message.guild
        voice_channel = server.voice_client
        addToQueue(ctx.message.guild, url)
        await playSong(ctx, voice_channel)
#Eventos
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="-ayuda"))
    print("Bot iniciado")
@bot.command()
async def binario(ctx, dato):
  """Transformador a binarios"""
  dato= bin(int (dato))
  await ctx.send(dato)
@bot.command()
async def sacar(ctx, user: discord.Member):
  """Desconecta al usuario"""
  await user.voice.channel.disconnect()


keep_alive()
bot.add_cog(Music(bot))

bot.run("")
