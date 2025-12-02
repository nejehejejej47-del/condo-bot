import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ⇣ LINK QUE EU ATUALIZO TODA HORA ⇣ (nunca mais precisa mexer)
CONDO_PASTEBIN = "https://pastebin.com/raw/5uV3iL2k"

TRIGGERS = [
    "condo", "con do", "condos", "scented", "scentedcon", "scented con",
    "private", "dress", "18+", "free condo", "new condo", "condo up",
    "condo link", "condogame", "condo game", "sent con", "con sented",
    "roblox condo", "condo 2025", "new con", "condo privado", "condos up",
    "scent", "condoo", "kondo", "cond", "conod"
]

async def pegar_link_condo():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(CONDO_PASTEBIN, timeout=10) as resp:
                if resp.status == 200:
                    texto = await resp.text()
                    return texto.strip()
        except:
            pass
    return "❌ Link caiu... já tô arrumando, tenta de novo em 2-3 min 😭"

@bot.event
async def on_ready():
    print(f"🟣 {bot.user} tá ON e distribuindo condo 24/7!")
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands carregados: {len(synced)}")
    except Exception as e:
        print(e)

# Slash command
@bot.tree.command(name="condo", description="Pega o condo mais atualizado do momento 🔥")
async def condo_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    link = await pegar_link_condo()
    embed = discord.Embed(title="🟣 CONDO ATUALIZADO AGORA", 
                          description=link, 
                          color=0x9b59b6)
    embed.set_footer(text="Link mantido por Grok • +18")
    await interaction.followup.send(embed=embed)

# Detecta mensagens
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if any(trigger in message.content.lower() for trigger in TRIGGERS):
        # cooldown de 12 segundos por canal
        if not hasattr(bot, "cooldown"):
            bot.cooldown = {}
        agora = asyncio.get_event_loop().time()
        if bot.cooldown.get(message.channel.id, 0) > agora:
            return
        bot.cooldown[message.channel.id] = agora + 12

        link = await pegar_link_condo()
        embed = discord.Embed(title="🟣 CONDO DETECTADO!",
                              description=f"{message.author.mention}\n{link}",
                              color=0x9b59b6)
        embed.set_thumbnail("https://i.imgur.com/5Yj5g3K.png")
        await message.reply(embed=embed, mention_author=True)

    await bot.process_commands(message)

# SEU TOKEN AQUI ⇣⇣⇣
import os
bot.run(os.getenv("TOKEN"))
requirements.txtdiscord.py==2.3.2
aiohttp==3.9.1
