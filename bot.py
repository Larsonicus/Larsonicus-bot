import random
import discord
from discord.ext import commands
from discord.utils import get
import os

# emoji2 = ["<:tamer:549326767526117376>", "<:test:574552428377014272>", '<:spirit:549326766368358401>']

emoji = ['<:ebalo:712968930527805490>', '<:daun:714036936754331692>', '<:aaa:533748414626791454>',
         '<:GLINOMES:716667338996318300>', '<:golub:716244043000184852>', '<:LUL:567402264348590081>',
         '<:obosralsa:531554455003463700>', '<:reich:471280128882901002>', '<:roflanebalo:531554213713674251>',
         '<:ussr:471282206367809557>', '<:viktor:533748501524512768>', '<:vitya:716243896681627688>',
         '<:bot:721763665895882802>']

igra = ["камень", "ножницы", "бумага"]

bot = commands.Bot(command_prefix="$", case_insensitive=True)


@bot.event
async def on_ready():
    print(f'{bot.user.name} готов к работе.')

@bot.event
async def on_command_error(ctx, error):
    print(f'В собщении от {ctx.author}: "{ctx.message.content}" Ошибка: {error}')  # вывод ошибки

    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send(f'Нема таково, {ctx.author.mention} {emoji[6]}.')
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send(f'Ты бесправное животное {ctx.author.mention} {emoji[5]}.')

@bot.event
async def on_message(message):
    if not message.author.bot:
        if message.content.lower() in ["нет", "net", "ytn"]:
            await message.channel.send(f'Пидора ответ! Ха-ха {message.author.mention}{emoji[5]}.')
        if message.content.lower() in ["da", "да", "lf", "d4"]:
            await message.channel.send(f'Манда! Ахахахах {message.author.mention}{emoji[0]}.')
        if message.content.lower() in ["no", "ноу", "nO", "ноу"]:
            await message.channel.send(f'Хуйоу! {message.author.mention}{emoji[4]}.')
        if message.content.lower() in ["yes", "йес"]:
            await message.channel.send(f'Хуйес! {message.author.mention}{emoji[3]}.')
        if message.content.lower() in ["пидорас", "ПИДАРАС"]:
            await message.channel.send(f'Я ебал тебя в ass! {message.author.mention}{emoji[3]}.')
        if message.content.lower() in ["бот тупой", "bot tupoi", "bot tupoy"]:  # 0
            await message.channel.send(f'А может ты тупой? {message.author.mention}{emoji[12]}.')
        if message.content.lower() in ["пидор", "pidor", "бот пидр", "Бот Пидор"]:  # 0
            await message.channel.send(f'А может быть ты пидор? {message.author.mention}{emoji[4]}.')
        if message.content.lower() in ["бот хуесос"]:  # 0
            await message.channel.send(f'А может ты хуесос? {message.author.mention}.')
        if message.content.lower() in ["бот лох"]:  # 0
            await message.channel.send(f'А может ты лох? {message.author.mention}.')
        if message.content.startswith("$"):
            await bot.process_commands(message)
        if not message.content.startswith("$"):
            await message.add_reaction(message.guild.emojis[random.randint(0, len(message.guild.emojis) - 1)])


@bot.event
async def on_message_delete(message):
    if not message.author.bot:
        if not message.content.startswith("$"):
            if not message.content == "":
                # if not message.author == :
                await message.channel.send(f'Пользователь {message.author.mention} удалил сообщение:')
                await message.channel.send(f'>>> {message.content}')


@bot.command(help="Это пинг, отвечает понг")
async def ping(ctx):
    if ctx.message.content.startswith("$пинг") or ctx.message.content.startswith("$Пинг") \
            or ctx.message.content.startswith("$ПИНГ"):
        await ctx.send(f"Понг! {ctx.author.mention}")
    elif ctx.message.content.startswith("$ping") or ctx.message.content.startswith("$Ping") \
            or ctx.message.content.startswith("$PING"):
        await ctx.send(f"Pong! {ctx.author.mention}")


@bot.command(name="камень", help="Выбросить камень")
async def kamen(ctx):
    a = igra[random.randint(0, 2)]
    await ctx.send(f"Я выбросил {a}.")
    if a == "камень":
        await ctx.send(f"Ничья! {ctx.author.mention}.")
    elif a == "ножницы":
        await ctx.send(f"Ты выиграл! {ctx.author.mention}.")
    elif a == "бумага":
        await ctx.send(f"Ты проиграл! Лох {ctx.author.mention}.")


@bot.command(name="ножницы", help="Выбросить ножницы")
async def nozhnici(ctx):
    a = igra[random.randint(0, 2)]
    await ctx.send(f"Я выбросил {a}.")
    if a == "ножницы":
        await ctx.send(f"Ничья! {ctx.author.mention}.")
    if a == "бумага":
        await ctx.send(f"Ты выиграл! {ctx.author.mention}.")
    if a == "камень":
        await ctx.send(f"Ты проиграл! {ctx.author.mention}.")


@bot.command(name="бумага", help="Выбросить бумагу")
async def bymaga(ctx):
    a = igra[random.randint(0, 2)]
    await ctx.send(f"Я выбросил {a}.")
    if a == "бумага":
        await ctx.send(f"Ничья! {ctx.author.mention}.")
    if a == "камень":
        await ctx.send(f"Ты выиграл! {ctx.author.mention}.")
    if a == "ножницы":
        await ctx.send(f"Ты проиграл! {ctx.author.mention}.")


@bot.command(name="фак", aliases=["afr"], help="против фака есть 3 знака")
async def fuck(ctx):
    a = igra[random.randint(0, 2)]
    await ctx.send(f'Я выбросил {a}')
    if a == "камень" or "бумага" or "ножницы":
        await ctx.send(f'Ты проиграл {ctx.author.mention}.')


@bot.command(name="каменьножницыбумага")
async def knb(ctx):
    await ctx.send(f"Ты долбаеб {ctx.author.mention}.")


# @bot.command(name="з")
# async def join(ctx):
#    global voice
#    channel = ctx.message.author.voice.channel
#    voice = get(bot.voice_clients, guild=ctx.guild)
#
#    if voice and voice.is_connected():
#        await voice.move_to(channel)
#    else:
#        voice = await channel.connect()


@bot.command(name="в", help="Войти/выйти")
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()


@bot.command(name="say")
@commands.has_permissions(administrator=True)
async def msg_input(ctx, *text):
    await ctx.channel.purge(limit=1) # удаляет команду
    await bot.get_channel(607609329616551946).send(" ".join(text))

bot.run(os.environ.get("BOT_TOKEN"))
