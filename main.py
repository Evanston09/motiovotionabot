# Import required modules
import discord
from discord.ext import commands
import random
import csv

# Define some global variables
csv_file = 'data.csv'
command_prefix = '.'
description = '''
# Set some global variables
Howdy, my name is **Motiovotionabot**
*Quote bot made and hosted by Evan Kim v0.1*
[Github Repo](https://github.com/Evanston09/motiovotionabot/)
'''

# Functions to interact with csv file
def store(csv_file_path, body, author):
    with open(csv_file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([body, author])

def is_file_empty(csv_file_path):
    with open(csv_file_path, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        return not any(csv_reader)

def pick_random(csv_file_path):
    with open(csv_file_path, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        data = [line for line in csv_reader]
    return random.choice(data)

# Retrieves token DO NOT SHARE
with open("token.txt", "r") as token_file:
    token = token_file.read().strip()

# Sets up intents and the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=command_prefix, intents=intents, description=description)

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
    store(csv_file, body, author)
    await ctx.send("Quote submitted successfully!!!")

# Define quote output
@bot.command()
async def quote(ctx):
    # Check if empty
    if is_file_empty(csv_file):
        await ctx.send("# No quotes have been submitted yet :frowning:\n__You can do that with **.submit [creative quote here]**__")
    # Find random quote and create a embed
    else:
        body,author = pick_random(csv_file)
        embed = discord.Embed(title="An inspirational quote for you :fire:", 
                         description=body,
                         color=discord.Color.from_rgb(42,82,190)
        )
        embed.add_field(name="Submitted by:", value=author, inline=True)
        embed.add_field(name="Want to submit your own?", value=".submit [your cool quote]", inline=True)
        await ctx.send(embed=embed)

# Run bot KEEP TOKEN A SECRET
bot.run(token)
