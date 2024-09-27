import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET-KEY')

intents = discord.Intents.default()
intents.members = True  # Pour écouter les événements liés aux membres
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="général")  # Assure-toi que le nom du canal est correct
    if channel is not None:
        embed = discord.Embed(
            title="Bienvenue !",
            description=f"Salut {member.mention}, bienvenue sur le serveur {member.guild.name} !",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url)  # Utilise l'avatar de l'utilisateur
        embed.set_footer(text=f"Nous sommes maintenant {member.guild.member_count} membres !")
        
        await channel.send(embed=embed)

# Exécute le bot
bot.run(SECRET_KEY)
