import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import io
import aiohttp

load_dotenv()
SECRET_KEY = os.getenv('SECRET-KEY')

intents = discord.Intents.default()
intents.members = True  # Pour écouter les événements liés aux membres
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')

# Fonction pour convertir une couleur hexadécimale en RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")  # Supprime le caractère # si présent
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))  # Convertit en RGB

async def create_welcome_image(member):
    # Chargement de l'image de fond
    background = Image.open("img/fond23-1.webp").convert("RGBA")

    # Récupération de l'avatar de l'utilisateur
    avatar_url = str(member.avatar.url)
    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as resp:
            avatar_data = await resp.read()
            avatar = Image.open(io.BytesIO(avatar_data)).convert("RGBA")

    # Redimensionner l'avatar
    avatar = avatar.resize((150, 150))  # Ajuste la taille selon tes besoins

    # Rendre l'avatar rond
    mask = Image.new("L", avatar.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 150, 150), fill=255)  # Crée un masque rond
    avatar.putalpha(mask)  # Applique le masque à l'avatar

    # Coller l'avatar sur l'image de fond
    avatar_position = (500, 50)  # Position de l'avatar
    background.paste(avatar, avatar_position, avatar)  # Colle l'avatar sur l'image de fond

    # Dessiner le pseudo de l'utilisateur en dessous de l'avatar
    draw = ImageDraw.Draw(background)

    # Charger une police avec une taille spécifique (Arial avec une taille de 80)
    font_size = 30  # Augmente la taille de la police
    try:
        font = ImageFont.truetype("arial.ttf", font_size)  # Assurez-vous que la police est disponible
    except IOError:
        font = ImageFont.load_default()  # Fallback si la police n'est pas trouvée

    # Couleur du texte (en hexadécimal)
    text_color_hex = "#FFED00"
    text_color_rgb = hex_to_rgb(text_color_hex)  # Convertir en RGB

    # Position du texte sous l'avatar
    text_position = (avatar_position[0] - 10, avatar_position[1] + avatar.size[1] + 10)  # Ajuste selon les besoins pour aligner à gauche

    # Dessiner l'ombre du texte
    shadow_offset = 3  # Décalage de l'ombre
    draw.text((text_position[0] + shadow_offset, text_position[1] + shadow_offset), member.name, fill=(0, 0, 0, 128), font=font)  # Ombre en noir
    draw.text(text_position, member.name, fill=text_color_rgb, font=font)  # Dessine le pseudo

    # Sauvegarde l'image dans un buffer
    buffer = io.BytesIO()
    background.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

@bot.event
async def on_member_join(member):
    channel_id = 1276609195591995514  # Remplace par l'ID du salon
    channel = bot.get_channel(channel_id)  # Récupère le salon par ID

    if channel is not None:
        image_buffer = await create_welcome_image(member)
        
        # Envoie l'image en tant que fichier
        await channel.send(file=discord.File(image_buffer, filename='welcome_image.png'))

        # Envoie le message de bienvenue après l'image
        message = f"Salut {member.mention}, bienvenue sur le serveur {member.guild.name} !"
        await channel.send(message)

# Exécute le bot
bot.run(SECRET_KEY)