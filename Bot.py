import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

sent_welcome = set()

class NumberSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="1", description="Select number 1", value="1"),
            discord.SelectOption(label="2", description="Select number 2", value="2"),
            discord.SelectOption(label="3", description="Select number 3", value="3"),
            discord.SelectOption(label="4", description="Select number 4", value="4"),
        ]
        super().__init__(placeholder="Choose a number...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

class NumberDropdown(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(NumberSelect())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_guild_join(guild):
    if guild.id in sent_welcome:
        return
    sent_welcome.add(guild.id)
    
    embed = discord.Embed(
        title="👋 Hello! Thanks for inviting me!",
        description="Please select a number from the dropdown menu below.",
        color=discord.Color.blurple()
    )
    embed.set_footer(text="Your custom bot here | Hacker mode coming soon...")
    
    channel = discord.utils.get(guild.text_channels, name='custom-bot')
    if channel and channel.permissions_for(guild.me).send_messages:
        await channel.send(embed=embed, view=NumberDropdown())
    else:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=embed, view=NumberDropdown())
                break

@bot.command()
async def testwelcome(ctx):
    embed = discord.Embed(
        title="👋 Hello! Thanks for running the test!",
        description="Please select a number from the dropdown menu below.",
        color=discord.Color.blurple()
    )
    embed.set_footer(text="Test message | Hacker mode coming soon...")
    await ctx.send(embed=embed, view=NumberDropdown())

# Use environment variable for token
bot.run(os.getenv('DISCORD_TOKEN'))
