from imp import *
from func import *

Bot = commands.Bot(command_prefix= "$$")

Bot.remove_command("help")

who_afk = {}


async def my_time():
    await Bot.wait_until_ready()
    moscow = datetime.now(timezone('Europe/Moscow')).strftime('%H:%M')  # Узнаем время по МСК
    channel = Bot.get_channel(564076987392458808)         # TIME CHANNEL  
    chan_bef = " ".join(channel.name.split()[0:-1])
    await channel.edit(name=f"{chan_bef} {moscow}")
    while not Bot.is_closed():
        moscow = datetime.now(timezone('Europe/Moscow')).strftime('%H:%M')
        chan_bef = " ".join(channel.name.split()[0:-1])
        await channel.edit(name=f"{chan_bef} {moscow}")
        await asyncio.sleep(60)


@Bot.event
async def on_ready():
    print("Online")

@Bot.event
async def on_voice_state_update(member, before, after):
    guild = Bot.get_guild(557164062144987136)   # Беру сервер
    channels = guild.channels  # Юеру все каналы
    v_channels = [channel for channel in channels if isinstance(channel, discord.VoiceChannel)]
    v_members = []
    for channel in v_channels:
        v_members.extend(channel.members) # Составляем список людей которые в войс каналах
    v_channel = Bot.get_channel(564082135187587120)   # Беру голосовой канал который мне нужен
    chan_bef = " ".join(v_channel.name.split()[0:-1])   # Берем навзвание канала которое было до этого и уберает последнюю позицию через массив
    await v_channel.edit(name= f"{chan_bef} {len(v_members)}") # редактирует канал на новое название с обновленной информацией

@Bot.event
async def on_member_update(before, after):
    guild = Bot.get_guild(557164062144987136)
    channel_o = Bot.get_channel(564086232104304652)
    chan_bef = " ".join(channel_o.name.split()[0:-1])
    online = [mem for mem in guild.members if mem.status is discord.Status.online]
    await channel_o.edit(name = f"{chan_bef} {len(online)}")


@Bot.event
async def on_message(msg):
    global who_afk
    if msg.author in who_afk and not msg.author.bot:
        try:
            await msg.author.edit(nick= who_afk[msg.author])
        except:
            pass
        await msg.channel.send(msg.channel, "{}**``is back``**".format(msg.author.mention))
        who_afk.pop(msg.author)
    try:
        await Bot.process_commands(msg)
    except Exception:
        pass

@Bot.command()
async def ping(ctx):
    msg = await ctx.send(f"**Pong** ``...``")
    await msg.edit(content= f"**Pong** ``{round(Bot.latency, 1)}``")

@Bot.command(pass_context= True)
async def help(ctx):
    try:
        await ctx.message.author.send(ctx.message.author, " **О, привет, знал что тебе будет инетерсно какие же тут команды, но к сожалению бот временно находится в разработке.\nТак что советую чуть-чуть подождать.\nУдачи ))**")
    except Exception:
        await ctx.send(f"{ctx.message.author.mention} **I don't think so )**")

@Bot.command(pass_context = True)
async def afk(ctx):
    """use it if you want to left in AFK"""
    global who_afk
    farewell = ctx.message.content.split(' ')[1:]
    if len(farewell) > 0:
        await ctx.send("{} **``left in afk with farewell:``** __``{}``__".format(ctx.message.author.mention, ' '.join(farewell)))
    else:
        await ctx.send("{} **``left in AFK``**".format(ctx.message.author.mention))
    try:
        who_afk[ctx.message.author] = ctx.message.author.display_name
        await ctx.message.author.edit(ctx.message.author, "AFK")
    except:
        pass
    await ctx.message.delete()

@Bot.command()
@commands.has_permissions(administrator= True)
async def info(ctx, user: discord.Member):
    """
Выводит информацию о пользователе
    """
    emb = add_fie(
        cemb(
                        f"Info about {user.name}", # Title
                        colour, # colour = переменная colour
                        ctx.message.author, # Footer
                        Bot.user), # Author
    {
        "Name": user.name, # Имя пользователя
        "ID": user.id, # ID Пользователя
        "Status": user.status, # 
        "Joined at": str(user.joined_at)[:16], # то когда пользователь пришел на сервер
        "Created at": str(user.created_at)[:16] # Когда был создан аккаунт
    })
    await ctx.send(embed= emb)

@Bot.group(pass_context= True)
@commands.has_permissions(administrator= True)
async def message(ctx):
    pass


@message.command(pass_context= True)
@commands.has_permissions(administrator= True)
async def embed(ctx):
    content = ctx.message.content.split("\n")[1:]
    # if content[-1].startswith("https"):
    #     image = True
    #     content.pop(-1)
    
    c_title = content[0]    # Title
    descp = "\n".join(content[1:])  # Description
    author = ctx.message.author # Author
    
    emb = discord.Embed(title= c_title, description= descp)
    
    # if image == True:
    #     emb.set_thumbnail(url= content[-1])

    await ctx.message.delete(ctx.message)
    await ctx.send(embed= emb)

Bot.loop.create_task(my_time())
Bot.run("NTU5NDk2MTgyNTM2MjA4Mzg2.XKi1JQ.pWXPsKm9yqrXEYxFgWvnqF__2DY")
