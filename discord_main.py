import discord
import discord_token
from discord.ext import commands
import requests
import random
from movies import dovus_filmleri, korku_filmleri, romantik_filmler

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents) #help_command=None

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık')
    
@bot.command()
async def help2(ctx):
    embed = discord.Embed(title="Bot Komutları", description="Bu bot filmlerle alakalı", color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command()
async def oneri(ctx):
    await ctx.send("Ne tür filmleri seversin? (dövüş, romantık, korku) ")
    while True:
        try:
            cevap_mesaji = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
            kullanici_sevdigi = cevap_mesaji.content
            if kullanici_sevdigi.upper() == 'DÖVÜŞ':
                film, konu = random.choice(list(dovus_filmleri.items()))
                await ctx.send(f"Sana {kullanici_sevdigi} filmlerinden {film} filmini önerebilirim.")
                await ctx.send(f"Filmin konusu: {konu}")
                dovus_filmleri.pop(film, konu)
                await ctx.send("Bu türde başka bir film izlemek ister miydin? (Evet/Hayır) ")
                devam_mesaji = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
                kullanici = devam_mesaji.content
                if kullanici.upper() == 'EVET':
                    for i in range(len(dovus_filmleri.items())):
                        film, konu = random.choice(list(dovus_filmleri.items()))
                        await ctx.send(f"Tür: {kullanici_sevdigi}, Film İsmi: {film}")
                        await ctx.send(f"Filmin konusu: {konu}")
                        dovus_filmleri.pop(film, konu)
                else:
                    break
                
            elif kullanici_sevdigi.upper() == 'ROMANTIK':
                film, konu = random.choice(list(romantik_filmler.items()))
                await ctx.send(f"Sana {kullanici_sevdigi} filmlerinden {film} filmini önerebilirim.")
                await ctx.send(f"Filmin konusu: {konu}")
                await ctx.send("Bu türde başka bir film izlemek ister miydin? (Evet/Hayır) ")
                romantik_filmler.pop(film, konu)
                await ctx.send("Bu türde başka bir film izlemek ister miydin? (Evet/Hayır) ")
                devam_mesaji = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
                kullanici = devam_mesaji.content
                if kullanici.upper() == 'EVET':
                    for i in range(len(romantik_filmler.items())):
                        film, konu = random.choice(list(romantik_filmler.items()))
                        await ctx.send(f"Tür: {kullanici_sevdigi}, Film İsmi: {film}")
                        await ctx.send(f"Filmin konusu: {konu}")
                        romantik_filmler.pop(film, konu)
                else:
                    break
                
            elif kullanici_sevdigi.upper() == 'KORKU':
                film, konu = random.choice(list(korku_filmleri.items()))
                await ctx.send(f"Sana {kullanici_sevdigi} filmlerinden {film} filmini önerebilirim.")
                await ctx.send(f"Filmin konusu: {konu}")
                korku_filmleri.pop(film, konu)
                await ctx.send("Bu türde başka bir film izlemek ister miydin? (Evet/Hayır) ")
                devam_mesaji = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
                kullanici = devam_mesaji.content
                if kullanici.upper() == 'EVET':
                    for i in range(len(korku_filmleri.items())):
                        film, konu = random.choice(list(korku_filmleri.items()))
                        await ctx.send(f"Tür: {kullanici_sevdigi}, Film İsmi: {film}")
                        await ctx.send(f"Filmin konusu: {konu}")
                        korku_filmleri.pop(film, konu)
                else:
                    break
            
        except:
            await ctx.send("Lütfen geçerli bir tür adı girin")
    

API_KEY = '98aeb406'


def search_movie(movie_name):
    url = "https://www.omdbapi.com/?t={}".format(movie_name)+f"&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        story_info = data["Plot"]
        return story_info
    else:
        return None
    
@bot.command()
async def story(ctx, *movie_name):
    full_movie_name = " ".join(movie_name)
    story_info = search_movie(full_movie_name)
    if story_info is not None:
        await ctx.send("Verilen filmin hikaye taslağı '{}' is: {}".format(full_movie_name, story_info))
    else:
        await ctx.send("Film için hikaye konusu bulunamadı '{}'".format(full_movie_name))
    
        
bot.run(discord_token.token)
