from imp import *
from func import *

Bot = commands.Bot(command_prefix= "$$")

Bot.remove_command("help")

who_afk = {}

@Bot.event
async def on_ready():
    pass

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

Bot.run(os.environ.get('BOT_TOKEN'))