from modules.__init__ import *
from modules.func import *

Bot = commands.Bot(command_prefix= "$$")

Bot.remove_command("help")

who_afk = {}


async def my_time():
    await Bot.wait_until_ready()
    channel = Bot.get_channel(559596558631436289)   # TIME CHANNEL

    moscow = datetime.now(timezone('Europe/Moscow')).strftime('%H:%M')  # Узнаем время по МСК
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
    await Bot.change_presence(status= discord.Status.dnd, activity= discord.Game("$$help"))

@Bot.event
async def on_voice_state_update(member, before, after):
    guild = Bot.get_guild(457617717755904011)   # Беру сервер
    channels = guild.channels  # Юеру все каналы
    vo_channel = Bot.get_channel(559601161368371200)   # Voice online channel

    v_channels = [channel for channel in channels if isinstance(channel, discord.VoiceChannel)]
    v_members = []
    for channel in v_channels:
        v_members.extend(channel.members) # Составляем список людей которые в войс каналах
    chan_bef = " ".join(vo_channel.name.split()[0:-1])   # Берем навзвание канала которое было до этого и уберает последнюю позицию через массив
    await vo_channel.edit(name= f"{chan_bef} {len(v_members)}") # редактирует канал на новое название с обновленной информацией


    duo_channel = Bot.get_channel(564913710704099328)   # Duo voice чат
    duo_category = Bot.get_channel(564913597013032961)  # туда куда будут создавваться duo каналы

    if after.channel == duo_channel:    # Человека бросит в только тчо созданный канал если он зайдет в нужный канал
        new_voice_channel = await duo_category.create_voice_channel("duo", user_limit = 2)
        await member.edit(voice_channel= new_voice_channel)


    if isinstance(before.channel, discord.VoiceChannel) and \
        before.channel.name == "duo" and \
            len(before.channel.members) < 1:   # Если в duo канале меньше 1 человека то он удаляется
        try:
            await before.channel.delete()
        except Exception:
            pass

        




@Bot.event
async def on_member_update(before, after):
    guild = Bot.get_guild(457617717755904011)
    channel_o = Bot.get_channel(559601147145617429)

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
async def choose(ctx, *choices: str):
    """Выбрать между несколькими вариантами"""
    await ctx.send(random.choice(choices))

@Bot.command(pass_context= True)
async def ping(ctx):
    """Проверить пинг"""
    msg = await ctx.send(f"**Pong** ``...``")
    await msg.edit(content= f"**Pong** ``{round(Bot.latency, 1)}``")

@Bot.command()
async def help(ctx):
    """Выводит это сообщение"""
    emb = cemb("Все команды", colour, ctx.message.author, Bot.user)
    for key, value in Bot.all_commands.items():
        if key not in adm_help:
            emb.add_field(name= key, value= value.help)

    try:
        
        await ctx.message.author.send(embed= emb)
    except Exception:
        async with ctx.message.channel.typing():
            await ctx.send(embed= emb,
            content= f"{ctx.message.author.mention}``, прости но я не могу тебе написать поэтому это сообщение скоро изчезнет чтобы не спамить...``",
            delete_after= 15)
    finally:
        await ctx.message.delete()

@Bot.command(pass_context = True)
async def afk(ctx):
    """Используй это если хочешь уйти в AFK"""
    global who_afk
    farewell = ctx.message.content.split(' ')[1:]
    if len(farewell) > 0:
        await ctx.send("{} **``left in afk with farewell:``** __``{}``__".format(ctx.message.author.mention, ' '.join(farewell)))
    else:
        await ctx.send("{} **``left in AFK``**".format(ctx.message.author.mention))
    try:
        who_afk[ctx.message.author] = ctx.message.author.display_name
        await ctx.message.author.edit(nick= "AFK")
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
async def say(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.message.channel.typing():
            content = ctx.message.content.split("\n")[1:]
            await ctx.send("\n".join(content))
            await ctx.message.delete()

@say.command(pass_context= True)
@commands.has_permissions(administrator= True)
async def embed(ctx):
    async with ctx.message.channel.typing():
        content = ctx.message.content.split("\n")[1:]
        
        c_title = content[0]    # Title
        descp = "\n".join(content[1:])  # Description
        emb = discord.Embed(title= c_title, description= str(descp), colour= colour)
        emb.set_footer(text= f"Написал {ctx.message.author.name}", icon_url= ctx.message.author.avatar_url)

        await ctx.send(embed= emb)
        await ctx.message.delete()

@say.command(pass_context= True)
@commands.has_permissions(administrator= True)
async def image(ctx):
    async with ctx.message.channel.typing():
        if not os.path.isdir("./files"):
            os.mkdir("files")
        dir = os.path.join("files/")
        att_name = ctx.message.attachments[0].filename
        path = dir + att_name
        await ctx.message.attachments[0].save(path)
        await ctx.send(file= discord.File(fp= path))
        os.remove(path)
        os.rmdir("files")
        await ctx.message.delete()


Bot.loop.create_task(my_time())
Bot.run(open("Bot/token.txt", 'r').read())
