import discord
from discord.ext import commands
from model import get_class
import os, random
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command(name='duck')
async def duck(ctx):
    '''The duck command returns the photo of the duck'''
    print('hello')
    image_url = get_duck_image_url()
    await ctx.send(image_url)


@bot.command()
async def check(ctx):
    await ctx.send("Please upload an image for me to analyze.")

    def check_message(message):
        return (
            message.author == ctx.author
            and message.channel == ctx.channel
            and len(message.attachments) > 0
        )

    try:
        message = await bot.wait_for(
            "message",
            check=check_message,
            timeout=60
        )

        attachment = message.attachments[0]

        file_name = attachment.filename
        file_url = attachment.url

        await attachment.save(f"./{file_name}")

        result = get_class(
            model_path="./keras_model.h5",
            labels_path="labels.txt",
            image_path=f"./{file_name}"
        )

        await ctx.send(result)

    except TimeoutError:
        await ctx.send("You took too long to upload an image :(")


bot.run('TU TOKEN AQUÍ')