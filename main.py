# Import required modules
import discord
from discord.ext import commands
import os
import random
import csv

# Define some global variables
admin = "<@821883083313381436>"
csv_file = 'data.csv'
command_prefix = '.'
description = '''
Howdy, my name is **Motiovotionabot**
*Quote bot made and hosted by Evan Kim v0.1*
[Github Repo](https://github.com/Evanston09/motiovotionabot/)
'''


# Functions to interact with csv file
def store(csv_file_path, body, author):
    with open(csv_file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([body, author])


# Check if non-existent or empty
def is_file_empty(csv_file_path):
    if not os.path.exists(csv_file_path):
        return True
    with open(csv_file_path, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        return not any(csv_reader)


# Pick random quote out of CSV
def pick_random(csv_file_path):
    with open(csv_file_path, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        data = [line for line in csv_reader]
    return random.choice(data)


def get_values(csv_file_path):
    values = []
    with open(csv_file_path, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            values.append(row)
    return values


# Retrieves token DO NOT SHARE
try:
    with open("token.txt", "r") as token_file:
        token = token_file.read().strip()
except FileNotFoundError:
    print("Add token in token.txt!")
    quit()

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
    # Check if empty or non-existent
    if is_file_empty(csv_file):
        await ctx.send(
            "# No quotes have been submitted yet :frowning:\n__You can do that with **.submit [creative quote here]**__")
    # Find random quote and create an embed
    else:
        body, author = pick_random(csv_file)
        embed = discord.Embed(title="An inspirational quote for you :fire:",
                              description=body,
                              color=discord.Color.from_rgb(42, 82, 190)
                              )
        embed.add_field(name="Submitted by:", value=author, inline=True)
        embed.add_field(name="Want to submit your own?", value=".submit [your cool quote]", inline=True)
        await ctx.send(embed=embed)


@bot.command()
async def query(ctx):
    author = ctx.message.author.mention
    if author == admin:
        await ctx.send(get_values('data.csv'))


# Run bot KEEP TOKEN A SECRET
try:
    bot.run(token)
except discord.errors.LoginFailure:
    print("Invalid token!")
