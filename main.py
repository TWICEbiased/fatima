#FATIMA, by Aurora Gómez
import time
import discord
import asyncio
from discord.ext import tasks
from hijri_converter import convert, Gregorian, Hijri
from discord.ext.commands import CommandNotFound
from discord.ui import Select, View
from linereader import copen
import random
from random import randint
from googletrans import Translator
from bs4 import BeautifulSoup
import requests
from discord.ext.commands import has_permissions
import datetime
import nacl
import variables
import pytz
from lxml import etree
import unidecode
import bolaocho
from discord import Option

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)
translator = Translator()
vc = None

@bot.event
async def on_ready():
    print("Assalamu Alaikum Wa Rahmatullahi Wa Barakatuh")
    while True:
      await set_date()
      await asyncio.sleep(1800)

async def set_date():
  hijri = get_current_hijri()
  await bot.change_presence(activity=discord.Game(name=f"{hijri}"))

def get_current_hijri():   
    hijri = convert.Gregorian.today().to_hijri()
    return f'{hijri.day} {hijri.month_name()} {hijri.year} {hijri.notation(language="en")}'


@bot.slash_command(name="date", description="Muestra la fecha en el calendario hijri.")
async def date(ctx):
  async with ctx.typing():
    await asyncio.sleep(1)
  hijri = get_current_hijri()
  await ctx.respond(hijri)

@bot.slash_command(name="hug", description="¡Abraza a tus amig@s!")
async def hug(ctx, member):
  async with ctx.typing():
    await asyncio.sleep(1)
  author = ctx.author.id
  if member == "<@1063221141465989173>":
    await ctx.respond("Jazak Allah Khair!")
  elif member == "<@" + str(author) + ">":
    await ctx.respond("¡<@" + str(author) + "> se ha abrazado a sí mism@!")
  else:
    embed = discord.Embed(title="Fatima", color=discord.Colour.random(), description="¡<@" + str(author) + "> ha abrazado a " + member + "!")
    linea = ""
    urls = []
    file = copen("abrazo.txt")
    lines = file.count('\n')
    for i in range (1, lines+1):
      laurl = file.getline(i)
      urls.append(laurl)
    urls = random.sample(urls, len(urls))
    linea = random.choice(urls)
    embed.set_image(url=linea)
    await ctx.respond(embed=embed)

@bot.slash_command(name="translate", description="¡Traduce de y a cualquier idioma! Para ver los idiomas disponibles, escribe /languages")
async def translate(ctx, message, language = ''):
    async with ctx.typing():
      await asyncio.sleep(1)
    if language == "":
        language = 'es'
    try:
      for key,value in variables.LANGUAGES.items():
        if language.lower() == value.lower():
          language = key
      if language.lower() == "chinese":
        language = 'zh-cn'
      elif language.lower() == "simplified chinese":
        language = 'zh-cn'
      elif language.lower() == "traditional chinese":
        language = 'zh-tw'
      for key,value in variables.LANGUAGESSP.items():
        value = unidecode.unidecode(value)
        language = unidecode.unidecode(language)
        if language.lower() == value.lower():
          language = key
      if language.lower() == "chino":
        language = 'zh-cn'
      elif language.lower() == "chino simplificado":
        language = 'zh-cn'
      elif language.lower() == "chino tradicional":
        language = 'zh-tw'
      else:
        translation = translator.translate(message, dest=language)
        traduccion = f"{translation.text}"
        idioma = f"{translation.src}"
        embed = discord.Embed(title="Traducción del " + variables.LANGUAGESSP[idioma] + " al " + variables.LANGUAGESSP[language] + ":",
                              color=discord.Colour.random(),
                              url="https://translate.google.com/?sl=auto&tl=" + language + "&text="+ message.replace(" ", "%20")
        )
        embed.add_field(name=f"{ctx.author.name} escribió:", value=message, inline=False)
        embed.add_field(name="Que se traduce a:", value=traduccion, inline=False)
        embed.set_thumbnail(url="https://cdn2.iconfinder.com/data/icons/web-store-crayons-volume-1/256/Language-512.png")
        await ctx.respond(embed=embed)
    except Exception as e:
      if str(e) == "invalid destination language":
        await ctx.respond("Discúlpame, no sé hablar `" + language +"`. Escribe /languages para ver la lista de idiomas disponibles.", ephemeral=True)
      else:
        await ctx.respond("Error: `" + str(e) + "`. This incident will be reported.", ephemeral=True)
        with open('log.txt', 'a') as file:
          file.write(str(datetime.datetime.now()) + " " + str(e) + ". Command used: " + "/translate " + message + " " + language)

@bot.slash_command(name="languages", description="Muestra los idiomas disponibles para traducción.")
async def languages(ctx):
  res = ""
  for values in variables.LANGUAGESSP.values():
    res = res + "\n" + values
  embed = discord.Embed(title="Idiomas disponibles",
                        description=res, 
                        color=discord.Colour.random())
  await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name="ping" ,description="Muestra la latencia del bot.")
async def ping(ctx):
  p = int(bot.latency * 1000)
  await ctx.respond("Pong! La latencia es " + str(p) + " ms")

@bot.slash_command(name="avatar", description="Muestra el avatar del usuario especificado.")
async def avatar(ctx, member=''):
  await ctx.defer()
  async with ctx.typing():
    await asyncio.sleep(1)
  try:
    if member == "":
      persona = ctx.author.name
      pfp = str(ctx.author.avatar)
      nombre3 = "Avatar de " + persona
      embed = discord.Embed(title=nombre3,
                            url=pfp,
                            color=discord.Colour.random())
                #username = user.name
      embed.set_image(url=pfp)
      await ctx.respond(embed=embed)
    else:
      miembro = []
      for letter in member:
        miembro.append(letter)
      del miembro[-1]
      del miembro[0]
      del miembro [0]
      mm = int(''.join(miembro))
      if mm == 1033494599852884130:
        await ctx.respond("No, ella no :3", ephemeral=True)
      else:
          usuario = await bot.fetch_user(mm)
          persona = usuario.name
          nombre3 = "Avatar de " + persona
          peticion = f"Pedido por: {ctx.author.name}"
          pfp = str(usuario.avatar)
          embed = discord.Embed(title=nombre3,
                                url=pfp,
                                color=discord.Colour.random())
                  #username = user.name
          embed.set_image(url=pfp)
          embed.set_footer(text=peticion)
          await ctx.respond(embed=embed)
  except:
    persona = ctx.author.name
    pfp = str(ctx.author.avatar)
    nombre3 = "Avatar de " + persona
    embed = discord.Embed(title=nombre3,
                          url=pfp,
                          color=discord.Colour.random())
                #username = user.name
    embed.set_image(url=pfp)
    await ctx.respond(embed=embed)    

@bot.slash_command(name="ball", description="Juego de preguntas.")
async def ball(ctx, question):
  respuestas = bolaocho.responses
  respuestas = random.sample(respuestas, len(respuestas))
  respuestas = random.sample(respuestas, len(respuestas))
  response = random.choice(respuestas)
  embed = discord.Embed(title=":8ball: Fatima 8ball",
                        color=discord.Colour.random())
  embed.add_field(name=f":question: {ctx.author.name} pregunta:",
                  value=question,
                  inline=False)
  embed.add_field(name=":100: Fatima responde:",
                  value=response,
                  inline=False)
  await ctx.respond(embed=embed)

@bot.slash_command(name="ayat", description="Envía la aleya especificada.")
async def ayat(ctx, surat, ayat, language=''):
  await ctx.defer()
  try:
    async with ctx.typing():
      await asyncio.sleep(2)
        # the target we want to open
    url = "https://legacy.quran.com/"+surat+"/"+ayat

        #open with GET method
    resp = requests.get(url)

        #http_respone 200 means OK status
    if resp.status_code == 200:

          # we need a parser,Python built-in HTML parser is enough .
      soup = BeautifulSoup(resp.text, 'html.parser')
      aleya = soup.find_all('span')
      araleya = soup.find_all('img')
      imagenar = str(araleya[20])
      imagenar2 = imagenar.split('src="')
      imagenar3 = str(imagenar2[1])
      arayat = imagenar3.split('"/>')
      texto = str(aleya[4].text)
      if language == '':
        language = "es"
      for key,value in variables.LANGUAGES.items():
        if language.lower() == value.lower():
            language = key
        if language.lower() == "chinese":
          language = 'zh-cn'
        elif language.lower() == "simplified chinese":
          language = 'zh-cn'
        elif language.lower() == "traditional chinese":
          language = 'zh-tw'
        for key,value in variables.LANGUAGESSP.items():
          value = unidecode.unidecode(value)
          if language.lower() == value.lower():
            language = key
        if language.lower() == "chino":
          language = 'zh-cn'
        elif language.lower() == "chino simplificado":
          language = 'zh-cn'
        elif language.lower() == "chino tradicional":
          language = 'zh-tw'
        else:
          translation = translator.translate(texto, dest=language)
          traduccion = f"{translation.text}"
          #await ctx.send(arayat[0])
          #await ctx.send(texto)
      embed = discord.Embed(title="Surat " + surat + " " + aleya[1].text + " Ayat " + ayat,
                      url="https://quran.com/" + surat + "/" + ayat,
                      color=discord.Colour.random())
      embed.set_image(url=arayat[0])
      embed.set_footer(text=traduccion)
      await ctx.respond(embed=embed)
  except Exception as e:
    if str(e) == "invalid destination language":
      await ctx.respond("Discúlpame, no sé hablar `" + language +"`. Escribe /languages para ver la lista de idiomas disponibles.", ephemeral=True)

@bot.slash_command(name="playsurat", description="Reproduce la sura y el rango de aleyas especificado.") #Quran recitations and FFMPEG must be downloaded separately.
async def playsurat(ctx, reciter: Option(str, choices=['Mishary Alafasy','Saad Al-Ghamdi', 'Abdul Basit Abdus Samad']), surat, initialayat='', finalayat='',  repetitions: int = 1):
  global vc
  rs = ""
  await ctx.respond("_ _", delete_after=1)
  try:
    for k in range(1, repetitions + 1):
      if reciter == 'Mishary Alafasy':
        rs = "mishari-rashid-al-afasy/"
      elif reciter == 'Saad Al-Ghamdi':
        rs = "saad-al-ghamdi/"
      elif reciter == 'Abdul Basit Abdus Samad':
        rs = "abdul-basit-abdus-samad/"
      if initialayat == "" or finalayat=="":
        if int(surat) < 10:
          surattt = "00" + surat
        elif int(surat) > 10 and int(surat) < 100:
          surattt = "0" + surat
        else:
          surattt = surat
        surah = variables.SURAT[str(surat)]
        voice_channel = ctx.author.voice.channel
        if voice_channel != None:
          vc = await voice_channel.connect()
          message = await ctx.send("Reproduciendo Surat " + str(int(surat)) + ": " + surah + ". Recitador: " + reciter + ". Repetición " + str(k) + "/" + str(repetitions) + ".  ﷽")
          vc.play(discord.FFmpegPCMAudio(executable="/home/container/ffmpeg/ffmpeg", source="/home/container/" + rs + surattt + ".mp3"))
          while vc.is_playing():
            await asyncio.sleep(.1)
          await vc.disconnect()
          await message.delete()
        else:
            await ctx.respond("¡" + str(ctx.author.name) + " no está en un canal de voz!", ephemeral = True, delete_after=10)
      else:
          j = ""
          if int(surat) < 10:
            suratt = "00" + surat
          elif int(surat) >= 10 and int(surat) < 100:
            suratt = "0" + surat
          else:
            suratt = surat
          voice_channel = ctx.author.voice.channel
          surah = variables.SURAT[str(surat)]
          if voice_channel != None:
            vc = await voice_channel.connect()
            message = await ctx.send("Reproduciendo Surat " + str(int(surat)) + ": " + surah + ", Ayat " + initialayat + "-" + finalayat + ". Recitador: " + reciter + ". Repetición " + str(k) + "/" + str(repetitions) + ". ﷽")
            for i in range(int(initialayat), int(finalayat) + 1):
              if i < 10:
                j = "00" + str(i) 
              elif i >= 10 and i < 100:
                j = "0" + str(i)
              else:
                j = str(i)
              vc.play(discord.FFmpegPCMAudio(executable="/home/container/ffmpeg/ffmpeg", source="/home/container/" + rs + "ayat/" + suratt + j + ".mp3"))
              while vc.is_playing():
                await asyncio.sleep(.1)
            await vc.disconnect()
            await message.delete()
  except AttributeError as e:
    if e == "'NoneType' object has no attribute 'is_playing'":
        pass
    else:
        await ctx.respond("¡Necesitas estar en un canal de voz para usar el comando!", ephemeral = True, delete_after=10)
  except discord.errors.ClientException as e:
    if e == "Not connected to voice.":
        pass
    else:
        await ctx.respond("¡Fatima ya está reproduciendo una Surat!", ephemeral = True, delete_after=10)

@bot.slash_command(name="stop", description="Desconecta al bot del canal de música.")
async def stop(ctx):
  try:
    await vc.disconnect()
    await ctx.respond("Desconectada.")
  except:
    await ctx.respond("¡Fatima no está en un canal de voz!", ephemeral = True)

@bot.slash_command(name="pic", description="¡Busca cualquier imagen de internet!")
async def pic(ctx, picture):
  await ctx.defer()
  resp = requests.get("https://www.bing.com/images/search?q=" + picture.replace(" ", "+"))
  soup = BeautifulSoup(resp.text, 'lxml')
  resimg = []
  for i in soup.find_all('img', {"class":"mimg rms_img"}):
    resimg.append(i['src'])
  res = random.sample(resimg, len(resimg))
  res = random.sample(res, len(res))
  url = random.choice(res)
  embed = discord.Embed(title="Buscador de imágenes: " + picture, 
                    url="https://www.bing.com/images/search?q=" + picture.replace(" ", "+"),
                    color=discord.Colour.random())
  embed.set_image(url=url)
  embed.set_footer(text=f"Requested by: {ctx.author.name}")
  await ctx.respond(embed=embed)

bot.run("TOKEN")