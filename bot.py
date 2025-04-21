import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive  # ⬅️ Webserver starten (für Replit wichtig)

# Keep-Alive-Webserver starten
keep_alive()

# .env laden
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Logging für Kontrolle
print("🔐 DISCORD_TOKEN geladen:", bool(DISCORD_TOKEN))
print("📺 CHANNEL_ID geladen:", CHANNEL_ID)

# Fehlerprüfung
if not DISCORD_TOKEN or not CHANNEL_ID:
    raise ValueError("❌ DISCORD_TOKEN oder CHANNEL_ID fehlt. Bitte .env-Datei prüfen!")

# Channel-ID casten
CHANNEL_ID = int(CHANNEL_ID)

# Bot-Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Ticket-Channel für Support
TICKET_CHANNEL_ID = 1325498324731564154

# View für Buttons
class ZahlungsmethodenButtons(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="💳 Mit PayPal (Eneba) kaufen", style=discord.ButtonStyle.primary, custom_id="paypal_button_unique")
    async def paypal_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "**Wähle eine der folgenden Optionen, um mit PayPal (Eneba) zu bezahlen:**\n\n"
            "➡️ [5$ Visa](https://www.eneba.com/rewarble-rewarble-visa-5-usd-voucher-global)\n"
            "➡️ [10$ Visa](https://www.eneba.com/rewarble-rewarble-visa-10-usd-voucher-global)\n"
            "➡️ [15$ Visa](https://www.eneba.com/rewarble-rewarble-visa-15-usd-voucher-global)\n"
            "➡️ [20$ Visa](https://www.eneba.com/rewarble-rewarble-visa-20-usd-voucher-global)\n"
            "➡️ [25$ Visa](https://www.eneba.com/rewarble-rewarble-visa-25-usd-voucher-global)\n"
            "➡️ [30$ Visa](https://www.eneba.com/rewarble-rewarble-visa-30-usd-voucher-global)\n"
            "➡️ [50$ Visa](https://www.eneba.com/rewarble-rewarble-visa-50-usd-voucher-global)\n"
            "➡️ [75$ Visa](https://www.eneba.com/rewarble-rewarble-visa-75-usd-voucher-global)\n"
            "➡️ [100$ Visa](https://www.eneba.com/rewarble-rewarble-visa-100-usd-voucher-global)\n"
            "➡️ [150$ Visa](https://www.eneba.com/rewarble-rewarble-visa-150-usd-voucher-global)\n\n"
            "Bitte klicke auf einen Link, um deinen Kauf abzuschließen.",
            ephemeral=True
        )

    @discord.ui.button(label="💸 Mit Krypto zahlen", style=discord.ButtonStyle.primary, custom_id="krypto_zahlen_unique")
    async def krypto_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "**Zahlung mit Kryptowährung:**\n"
            "TRX Wallet: TD275iwYieYwgHeAZdikwK6eqWVU7F6Fmf\n"
            "LTC Wallet: ltc1qajkretfz62ja9mnlnvzstwcughgazzavvdu8zu\n\n"
            "📸 Bitte sende einen Screenshot deiner Überweisung.\n"
            "Danach klicke auf **„Zahlung abgeschlossen“**.",
            ephemeral=True
        )

    @discord.ui.button(label="✅ Zahlung abgeschlossen", style=discord.ButtonStyle.success, custom_id="zahlung_abgeschlossen_unique")
    async def done_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket_channel = interaction.guild.get_channel(TICKET_CHANNEL_ID)
        await interaction.response.send_message(
            f"✅ Bitte öffne ein Ticket im Channel {ticket_channel.mention}, um deine Zahlung abzuschließen.\n"
            "Klicke dort auf **„Buy“**, um dein Ticket zu erstellen.",
            ephemeral=True
        )

@bot.event
async def on_ready():
    print(f"✅ {bot.user.name} ist online und bereit für Zahlungen.")

@bot.command()
async def zahlung(ctx):
    if ctx.channel.id != CHANNEL_ID:
        return await ctx.send("❌ Dieser Befehl darf nur im vorgesehenen Zahlungs-Channel verwendet werden.")

    embed = discord.Embed(
        title="🧾 Zahlungsmöglichkeiten",
        description=(
            "Hier kannst du Guthaben kaufen, um im Shop zu bezahlen.\n\n"
            "**🔹 Eneba (PayPal, Kreditkarte):**\n"
            "Wähle diese Option, um deine Zahlung per PayPal oder Kreditkarte abzuschließen.\n\n"
            "**🔹 Kryptowährungen:**\n"
            "Zahle sicher und schnell mit Kryptowährungen wie TRX und LTC.\n\n"
            "**❗ Hinweise:**\n"
            "• Nutze Rewarble Visa Karten bei PayPal-Zahlungen\n"
            "• Bei Krypto bitte Screenshot senden\n"
            "• Ticket nach Zahlung über den Button erstellen"
        ),
        color=discord.Color.blurple()
    )

    view = ZahlungsmethodenButtons()
    await ctx.send(embed=embed, view=view)

# Bot starten
bot.run(DISCORD_TOKEN)
