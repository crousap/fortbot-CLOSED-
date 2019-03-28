from imp import *
from func import *

Bot = commands.Bot(command_prefix= "$$")

Bot.remove_command("help")

who_afk = {}


async def my_time():
    await Bot.wait_until_ready()
    moscow = datetime.now(timezone('Europe/Moscow')).strftime('%H:%M')  # Узнаем время по МСК
    channel = Bot.get_channel("559596558631436289")         # TIME CHANNEL  
    chan_bef = " ".join(channel.name.split()[0:-1])
    await Bot.edit_channel(channel, name=f"{chan_bef} {moscow}")
    while not Bot.is_closed:
        moscow = datetime.now(timezone('Europe/Moscow')).strftime('%H:%M')
        chan_bef = " ".join(channel.name.split()[0:-1])
        await Bot.edit_channel(channel, name=f"{chan_bef} {moscow}")
        await asyncio.sleep(60)


@Bot.event
async def on_ready():
    print("Online")

@Bot.event
async def on_voice_state_update(before, after):
    server = Bot.get_server("457617717755904011")   # Беру сервер
    channels = server.channels  # Юеру все каналы
    v_channels = [channel for channel in channels if channel.type == discord.ChannelType.voice] # СОздается массив с каналами типа voice
    v_members = []
    for channel in v_channels:
        v_members.extend(channel.voice_members) # Составляем список людей которые в войс каналах
    v_channel = Bot.get_channel("559601161368371200")   # Беру голосовой канал который мне нужен
    chan_bef = " ".join(v_channel.name.split()[0:-1])   # Берем навзвание канала которое было до этого и уберает последнюю позицию через массив
    await Bot.edit_channel(v_channel, name= f"{chan_bef} {len(v_members)}") # редактирует канал на новое название с обновленной информацией

@Bot.event
async def on_member_update(before, after):
    server = Bot.get_server("457617717755904011")
    channel_o = Bot.get_channel("559601147145617429")
    chan_bef = " ".join(channel_o.name.split()[0:-1])
    online = [mem for mem in server.members if mem.status == discord.Status.online]
    await Bot.edit_channel(channel_o, name = f"{chan_bef} {len(online)}")


@Bot.event
async def on_message(msg):
    global who_afk
    if msg.author in who_afk and not msg.author.bot:
        try:
            await Bot.change_nickname(msg.author, who_afk[msg.author])
        except:
            pass
        await Bot.send_message(msg.channel, "{}**``is back``**".format(msg.author.mention))
        who_afk.pop(msg.author)
    try:
        await Bot.process_commands(msg)
    except Exception:
        pass

@Bot.command(pass_context= True)
async def ping(ctx):
    await Bot.say("Pong")

@Bot.command(pass_context= True)
async def help(ctx):
    try:
        await Bot.send_message(ctx.message.author, " **О, привет, знал что тебе будет инетерсно какие же тут команды, но к сожалению бот временно находится в разработке.\nТак что советую чуть-чуть подождать.\nУдачи ))**")
    except Exception:
        await Bot.say(f"{ctx.message.author.mention} **I don't think so )**")

@Bot.command(pass_context = True)
async def afk(ctx):
    """use it if you want to left in AFK"""
    global who_afk
    farewell = ctx.message.content.split(' ')[1:]
    if len(farewell) > 0:
        await Bot.say("{} **``left in afk with farewell:``** __``{}``__".format(ctx.message.author.mention, ' '.join(farewell)))
    else:
        await Bot.say("{} **``left in AFK``**".format(ctx.message.author.mention))
    try:
        who_afk[ctx.message.author] = ctx.message.author.display_name
        await Bot.change_nickname(ctx.message.author, "AFK")
    except:
        pass
    await Bot.delete_message(ctx.message)

@Bot.command(pass_context= True)
async def whovoice(ctx):
    channels = ctx.message.server.channels
    v_channels = [channel for channel in channels if channel.type == discord.ChannelType.voice]
    v_members = []
    for channel in v_channels:
        v_members.extend(channel.voice_members)
    await Bot.say('``' + "Now in voice " + str(len(v_members)) + " peoples" + '``')

@Bot.command(pass_context= True)
async def info(ctx, user: discord.User):
    emb = add_fie(cemb(f"Info about {user.name}", colour, ctx.message.author, Bot.user), {
        "Name": user.name,
        "ID": user.id,
        "Status": user.status,
        "Joined at": str(user.joined_at)[:16],
        "Created at": str(user.created_at)[:16]
    })
    await Bot.say(embed=emb)

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

    await Bot.delete_message(ctx.message)
    await Bot.say(embed= emb)

Bot.loop.create_task(my_time())
Bot.run(os.environ.get('BOT_TOKEN'))
