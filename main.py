import discord, uuid, requests, shutil, PIL
from discord.ext import commands
from discord import File
from PIL import Image, ImageDraw, ImageFont

client = commands.Bot(command_prefix = 'on ', intents = discord.Intents.all())

@client.event
async def on_ready():
    print("Bot is ready!")

@client.command()
async def save(ctx):
    try:
        url = ctx.message.attachments[0].url
    except IndexError:
        await ctx.send("No attachments!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":
            r = requests.get(url, stream=True)
            imageName = "original.png"
            with open(imageName, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)

            bg = Image.open("original.png")
            fg = Image.open("element.png")

            bg.paste(fg, (0,0), fg)
            bg.save("draft.png", format = "png")
            await ctx.send("Draft Image Saved!")

@client.command()
async def text(ctx,*, write:str):

    file_name = "draft.png"

    text_img = Image.open(file_name)

    image_editable = ImageDraw.Draw(text_img)

    text = write

    titlefont = ImageFont.truetype('font.otf', 60)

    width, height = 1200, 1200

    image_editable.text((width/2,height/1.07), text, (255,255,255), font = titlefont, anchor = "mm")
    text_img.save("news.png", format = "png")
    await ctx.send("Process completed!")

    final_file="news.png"
    await ctx.send(file=File(final_file))
    
    client.run(os.getenv('TOKEN'))
