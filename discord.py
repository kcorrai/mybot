import discord
import discord_token
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents) #help_command=None

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık')
    
@bot.command()
async def help2(ctx):
    embed = discord.Embed(title="Bot Komutları", description="Bu bot filmlerle alakalı", color=discord.Color.green())
    await ctx.send(embed=embed)
    
dovus_filmleri = {"Kung Fu Panda" : "Panda Po, kung fu hayranıdır. Ancak ailesine ait makarna restoranında çalışır ve bu spora pek yatkın sayılmaz. Hiç beklemediği bir anda eski bir kehanetin gereğini yerine getirmek için görevlendirilince Po'nun hayalleri gerçeğe dönüşür.",
                  "Fight Club" : "Başkarakterin insomnia hastalığı ile olan mücadelesini ele alır. Doktorunun görüşüne göre insomniadan muzdarip değil ve rahatlığı çeşitli destek gruplarında hasta bir kişiymiş gibi katılarak buluyor. Sonradan, Tyler Durden adında bir adamla tanışıyor ve psikoterapi amaçlı dövüş kulübünü başlatıyor.",
                  "The Karate Kid" : "12 yaşındaki Dre Parker, babasını küçük yaşta kaybetmiştir. Annesi ve Parker, annesinin işleri nedeniyle yaşadığı Detroit'ten Çin'in başkenti Pekin'e taşınmak zorunda kalır. Kültür farklılığının ve dil bilmenin zorluluğunu yaşayan Parker, ortama uyum sağlamaya çalışır."}

romantik_film = {""}
                    
bot.run(discord_token.token)
