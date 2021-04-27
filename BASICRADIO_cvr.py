import discord
from discord import FFmpegPCMAudio
from discord.ext import commands, tasks
from dotenv import load_dotenv
linkradio = "Ingresa aquí el enlace de la radio a utilizar"
tokendiscord = "Ingresa aquí el token del bot"
load_dotenv()
bot = commands.Bot(command_prefix = "tit", description="Tan solo una radio simple")

@bot.command()
async def o_creditos(ctx):
    embed = discord.Embed(title=f"Info", description="Deja un mensaje aquí:D", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://i.postimg.cc/GpVvGZYT/Whats-App-Image-2021-04-21-at-15-27-06.jpg")
    await ctx.send(embed=embed)
    print(ctx.guild.name)

@bot.command()
async def o(ctx):
    embed = discord.Embed(title=f"Listado Comandos", description="tito_creditos\n-tito_radio", color=discord.Color.red() )
    embed.set_thumbnail(url=f"https://i.postimg.cc/GpVvGZYT/Whats-App-Image-2021-04-21-at-15-27-06.jpg")
    await ctx.send(embed=embed)
    print(ctx.guild.name)
@bot.command()
async def o_radio(ctx, url: str = linkradio):
    embed = discord.Embed(title=f"COOOOOOO", description="`Radio Encendida! Escuchando radio X`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://i.postimg.cc/GpVvGZYT/Whats-App-Image-2021-04-21-at-15-27-06.jpg")
    await ctx.send(embed=embed)
    print(ctx.guild.name+" radio")
    channel = ctx.message.author.voice.channel
    global player
    try:
        player = await channel.connect()
    except:
        pass
    player.play(FFmpegPCMAudio(linkradio))


@bot.command()
async def o_stop(ctx):
    channel = ctx.message.author.voice.channel
    player = await channel.connect()
    player.stop()
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()
    embed = discord.Embed(title=f"COOOOOOO", description="`Radio Apagada`", color=discord.Color.blue() )
    embed.set_thumbnail(url=f"https://i.postimg.cc/GpVvGZYT/Whats-App-Image-2021-04-21-at-15-27-06.jpg")
    await ctx.send(embed=embed)
    print(ctx.guild.name+" radio apagada")

#Eventos
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Como usas la radio de CVR"))
    print("Iniciado")

bot.run(tokendiscord)
