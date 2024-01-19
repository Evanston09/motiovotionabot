# Requires messages intent

# Import required modules
import discord
import random
from discord.ext import commands
from quote import Quote

# Set some global variables
quotes = []
description = '''
Howdy my name is **Motiovotionabot**
*Quote bot made and hosted by Evan Kim v0.1*
'''
token = open("token.txt", "r")

# Sets up intents and the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents, description=description)

# Define description
@bot.command()
async def whoareyou(ctx):
    await ctx.send(bot.description)

# Submission
@bot.command()
async def submit(ctx):
    # Get quote information
    body = ctx.message.content[8:]
    author = ctx.message.author.mention

    # Check if empty
    if len(body) == 0:
        await ctx.send("You silly goose you didn't submit a quote:man_facepalming:")
        return

    # Store quote
    quotes.append(Quote(body, author))
    await ctx.send("Quote submitted successfully!!!")

# Define quote output
@bot.command()
async def quote(ctx):
    # Check if empty
    if not quotes:
        await ctx.send("# No quotes have been submitted yet :(\n__You can do that with **.submit [creative quote here]**__")
    # Find random quote and create a embed
    else:
        chosen = random.choice(quotes)
        embed = discord.Embed(title="An inspirational quote for you :fire:", 
                         description=chosen.body,
                         color=discord.Color.from_rgb(42,82,190))   
        embed.add_field(name="Submitted by:", value=chosen.author, inline=True)
        embed.add_field(name="Want to submit your own?", value=".submit [your cool quote]", inline=True)
        await ctx.send(embed=embed)

# Run bot keep token a secret
bot.run(token.read())
