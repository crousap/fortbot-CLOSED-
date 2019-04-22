from modules.__init__ import *
from modules.func import *

prefix = cfg['prefix']

Bot = commands.Bot(command_prefix= prefix)

Bot.remove_command("help")

who_afk = {}


async def my_time():
    await Bot.wait_until_ready()
    channel = Bot.get_channel(cfg['channel']['widget']['time'])   # TIME CHANNEL

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
    await Bot.change_presence(status= discord.Status.dnd, activity= discord.Game(f"{prefix}help"))

@Bot.event
async def on_voice_state_update(member, before, after):
    guild = Bot.get_guild(cfg['guild'])   # Беру сервер
    channels = guild.channels  # Юеру все каналы
    vo_channel = Bot.get_channel(cfg['channel']['widget']['online_voice'])   # Voice online channel

    v_channels = [channel for channel in channels if isinstance(channel, discord.VoiceChannel)]
    v_members = []
    for channel in v_channels:
        v_members.extend(channel.members) # Составляем список людей которые в войс каналах
    chan_bef = " ".join(vo_channel.name.split()[0:-1])   # Берем навзвание канала которое было до этого и уберает последнюю позицию через массив
    await vo_channel.edit(name= f"{chan_bef} {len(v_members)}") # редактирует канал на новое название с обновленной информацией


#----------------------------------------VOICE ONLINE---------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------LOBBY SYSTEM---------------------------------------------------------------------------------------------


    lobbys = cfg['channel']['lobby']
    id_of_channels = [i['channel_id'] for i in lobbys.values()]

    try:
        if after.channel.id in id_of_channels:  # Создает и перебрасывает
            for name in lobbys:
                if after.channel.id == lobbys[name]['channel_id']:
                    c_name = lobbys[name]['create_name']
                    limit = lobbys[name]['limit']
                    category = Bot.get_channel(lobbys[name]['category_id'])
                    new_voice_channel = await category.create_voice_channel(c_name, user_limit = limit)
                    await member.edit(voice_channel= new_voice_channel)
                    break
    except AttributeError:
        pass

    names = [name['create_name'] for name in lobbys.values()]
    categorys = [n['category_id'] for n in lobbys.values()]
    try:
        if before.channel.name in names and before.channel.category.id in categorys:
            for name in lobbys:
                if before.channel.category.id == lobbys[name]['category_id']:
                    limit = lobbys[name]['limit']
                    break

            if len(before.channel.members) == 0:    # Удаляет если пустой
                await before.channel.delete()
            elif len(before.channel.members) < limit:  # Делает канал видимым
                everyone = discord.utils.get(before.channel.guild.roles, name= '@everyone')
                await before.channel.set_permissions(everyone, read_messages= True)
    except AttributeError:
        pass
    try:
        if after.channel.name in names and after.channel.category.id in categorys:
            for name in lobbys:
                if after.channel.category.id == lobbys[name]['category_id']:
                    limit = lobbys[name]['limit']
                    break

            if len(after.channel.members) >= limit:
                everyone = discord.utils.get(after.channel.guild.roles, name= '@everyone')
                await after.channel.set_permissions(everyone, read_messages= False)
    except AttributeError:
        pass

@Bot.event
async def on_command_error(ctx, error):
    ctx_command = str(ctx.message.content.split(" ")[0])
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author.mention} ``Прости ,но команды нету ¯\_(ツ)_/¯``", 
                        delete_after= 3)
    
    elif isinstance(error, commands.BadArgument) and (ctx_command == (f"{prefix}report")):
# Если в комманде недописали аргумент, и сама команда report 

        msg_content = \
f"""``
О, я вижу то, что ты хочешь кинуть на кого-то репорт, спотри как надо это делать:``
\n{prefix}report {Bot.user.mention} \"Он слишком хорош !\"
\n``Заметь что сама жалоба находиться в двойных кавычках``
"""
        await ctx.send(msg_content, delete_after= 15)
        await ctx.message.delete()

@Bot.event
async def on_member_update(before, after):
    guild = Bot.get_guild(cfg['guild'])
    channel_o = Bot.get_channel(cfg['channel']['widget']['online'])

    chan_bef = " ".join(channel_o.name.split()[0:-1])
    online = [mem for mem in guild.members if mem.status is discord.Status.online]
    await channel_o.edit(name = f"{chan_bef} {len(online)}")


@Bot.event
async def on_message(msg):
    global who_afk
    if msg.author == Bot.user:
        pass

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

@Bot.command()
async def report(ctx, user: discord.User, desc):
    """Отправить репорт на кого-то"""
    report_channel = Bot.get_channel(cfg['channel']['report']) # Deff report channel

    emb = add_fie(  # Создаем embed
        cemb(
            "Жалоба", 
            colour,
            ctx.message.author,
            Bot.user),
            {
                "Виновник": user.mention,
                "Провинился в": desc
            })

    emb.set_footer(text=f"Отправил жалобу {ctx.message.author.display_name}", 
                    icon_url= ctx.message.author.avatar_url) # Ставим автора в конце

    msg = await report_channel.send(embed= emb)
    temp_msg = await ctx.send(f"``Спасибо ``{ctx.message.author.mention}`` за то, что способствуешь улучшению коммьюнити сервера``")

    await asyncio.sleep(10)
    await ctx.message.channel.delete_messages([temp_msg, ctx.message])
    



Bot.loop.create_task(my_time())
Bot.run(open("token.txt", 'r').read())
