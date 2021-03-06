import random
import discord
from discord.ext import commands
import os
import logging
import requests
from bs4 import BeautifulSoup

game = ["камень", "ножницы", "бумага"]

blacklist = os.environ.get("BLACK_TAGS", open("blacklist.txt").readlines())
blacktags = ''
for i in blacklist:
    blacktags += i.rstrip('\n')

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4414.0 '
                         'Safari/537.36 Edg/90.0.803.0', 'accept': '*/*'}

HOST = 'https://rule34.xxx/'

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="$", case_insensitive=True)


@bot.event
async def on_ready():
    print(f'{bot.user.name} готов к работе.')


@bot.event
async def on_command_error(ctx, error):
    print(f'В собщении от {ctx.author}: "{ctx.message.content}" Ошибка: {error}.')  # вывод ошибки

    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send(f'Данной команды не существует, {ctx.author.mention}.')
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send(f'Ты бесправное животное {ctx.author.mention}.')


@bot.event
async def on_message(message):
    if not message.author.bot:
        if message.content.lower() in ["нет", "net", "ytn"]:
            await message.channel.send(f'Пидора ответ! Ха-ха {message.author.mention}.')
        if message.content.lower() in ["da", "да", "lf"]:
            await message.channel.send(f'Манда! Ахахахах {message.author.mention}.')
        if message.content.startswith("$"):
            await bot.process_commands(message)
        '''if not message.content.startswith("$"):  # реакция на сообщение
            await message.add_reaction(message.guild.emojis[random.randint(0, len(message.guild.emojis) - 1)])'''


@bot.event
async def on_message_delete(message):  # также добавить, когда юзер изменяет сообщение
    if not message.author.bot:
        if message.content.startswith("$") or message.content.startswith(";;"):
            return None
        if not message.content == "":
            await message.channel.send(f'Пользователь {message.author.mention} удалил сообщение:')
            await message.channel.send(f'>>> {message.content}')


@bot.command(name="ping", aliases=["пинг"], help="Это пинг, отвечает понг")
async def ping(ctx):
    if ctx.message.content.lower().startswith("$ping"):
        await ctx.send(f"Pong! {ctx.author.mention}.")
    elif ctx.message.content.lower().startswith("$понг"):
        await ctx.send(f"Понг! {ctx.author.mention}.")


@bot.command(name="rock", aliases=["камень"], help="Выбросить камень")
async def rock(ctx):
    a = game[random.randint(0, 2)]
    await ctx.send(f"Я выбросил {a}.")
    if a == "камень":
        await ctx.send(f"Ничья! {ctx.author.mention}.")
    elif a == "ножницы":
        await ctx.send(f"Ты выиграл! {ctx.author.mention}.")
    else:
        await ctx.send(f"Ты проиграл! {ctx.author.mention}.")


@bot.command(name="scissors", aliases=["ножницы"], help="Выбросить ножницы")
async def scissors(ctx):
    a = game[random.randint(0, 2)]
    await ctx.send(f"Я выбросил {a}.")
    if a == "ножницы":
        await ctx.send(f"Ничья! {ctx.author.mention}.")
    elif a == "бумага":
        await ctx.send(f"Ты выиграл! {ctx.author.mention}.")
    else:
        await ctx.send(f"Ты проиграл! {ctx.author.mention}.")


@bot.command(name="paper", aliases=["бумага"], help="Выбросить бумагу")
async def paper(ctx):
    a = game[random.randint(0, 2)]
    await ctx.send(f"Я выбросил {a}.")
    if a == "бумага":
        await ctx.send(f"Ничья! {ctx.author.mention}.")
    elif a == "камень":
        await ctx.send(f"Ты выиграл! {ctx.author.mention}.")
    else:
        await ctx.send(f"Ты проиграл! {ctx.author.mention}.")


def get_image(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='flexi')
    image = ''
    try:
        for i in items:
            image = (i.find('img', alt_='').get('src'))
    except AttributeError:  # if video
        videos = soup.find_all('source')
        for video in videos:
            image = (video.get('src'))
    return image


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('span', class_='thumb')
    links = []
    for i in items:
        links.append(HOST + i.find('a').get('href'))
    return links


async def send_image(ctx, pages):
    html = get_html(random.choice(pages))
    posts_links = get_content(html.text)
    image_link = random.choice(posts_links)
    html = get_html(image_link)
    await ctx.send(get_image(html.text))


def get_pages_links(url, html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('div', class_='pagination')
    try:
        p = pagination.find_all('a')
        pages = [url]
        for page in p:
            pages.append(HOST + (page.get('href')))
        if len(pages) >= 11:
            del pages[-2:]
    except AttributeError:  # по заданному tag нет страниц
        pages = 0
    return pages


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def try_except(*taa):
    amount = 1
    tag = ''
    try:
        amount = int(taa[0])
    except ValueError:
        tag = taa[0]
    except IndexError:
        tag = tag
        print(tag)
    try:
        amount = int(taa[-1])
    except IndexError:  # taa не указан
        pass
    except ValueError:
        try:
            amount = int(taa[0])
            tag = taa[1]
        except ValueError:
            tag = taa[0]
    list_taa = [tag, amount]
    return list_taa


@bot.command(name="full", aliases=["фулл"], help="Скидывает фулл", pass_context=True)
async def parse(ctx, *taa):  # taa - tag and amount
    if len(taa) > 2:
        return await ctx.send(f'Введите корректный запрос {ctx.author.mention}.')
    list_taa = try_except(*taa)
    tag = list_taa[0]
    amount = list_taa[1]
    url = f'https://rule34.xxx/index.php?page=post&s=list&tags={tag}{blacktags}'
    html = get_html(url)
    pages_links = get_pages_links(url, html.text)
    if pages_links == 0:
        return await ctx.send(f'Введите корректный запрос {ctx.author.mention}.')
    if amount > 100:
        return await ctx.send(f'Не больше 100 картинок! {ctx.author.mention}.')
    elif amount < 0:
        return await ctx.send(f'Не меньше 0 картинок! {ctx.author.mention}.')
    pages = []
    for page in pages_links:
        pages.append(page)
    for a in range(amount):
        await send_image(ctx, pages)


@bot.command(name='tags')
async def tags_help(ctx):  # улучшить
    taglist = os.environ.get("TAGS", open("taglist.txt").readlines())
    tags = ''
    for i in taglist:
        tags += f'\t{i}'
    await ctx.send(f'```Классные тэги:\n{tags}```')


@bot.command(name='purge', help='Удаляет необходимое количество сообщений из канала.', hidden=True)
@commands.has_permissions(administrator=True)
async def purge_message(ctx, limit: int):
    await ctx.channel.purge(limit=limit)


bot.run(os.environ.get("BOT_TOKEN"))
