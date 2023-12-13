import discord
import discord_token
from discord.ext import commands
import requests
import random
from movies import dovus_filmleri, korku_filmleri, romantik_filmler, testler

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None) #help_command=None

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık')
    
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Bot Komutları", color=discord.Color.green())
    embed.add_field(name="!filmöner", value="Sana sevdiğin film türlerine göre film tavsiyesinde bulunur.", inline=False)
    embed.add_field(name="!filmara", value="Aramak istediğin filmin konusunu, inceleme puanını, posterlerini vs. gösterir. NOT: İşlemi çağırdıktan sonra aranmak istenen film adı yazılmalıdır")
    embed.add_field(name="!filmtesti", value="Sana film bilgilerini test edebilecek birçok farklı web sitesi gösterir.")
    await ctx.send(embed=embed)

@bot.command()
async def filmöner(ctx):
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
    

API_KEY = 'api key from OMDb API'


def search_movie(movie_name):
    url = "https://www.omdbapi.com/?t={}".format(movie_name)+f"&apikey={API_KEY}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        movie_plot = data["Plot"]
        movie_rating = data["imdbRating"]
        movie_poster = data["Poster"]
        return [movie_plot, movie_rating, movie_poster]
    else:
        return None
    
@bot.command()
async def filmara(ctx, *movie_name):
    full_movie_name = " ".join(movie_name)
    story_info = search_movie(full_movie_name)
    if story_info is not None:
        await ctx.send("Verilen filmin hikaye taslağı '{}' is: {}".format(full_movie_name, story_info[0]))
        await ctx.send(f"IMDb Puanı: {story_info[1]}")
        await ctx.send(story_info[2])
    else:
        await ctx.send("Film bulunamadı '{}'".format(full_movie_name))
        
@bot.command()
async def filmtesti(ctx):
    link, aciklama = random.choice(list(testler.items()))
    await ctx.send(f"{aciklama} => {link}")    
        
bot.run(discord_token.token)
