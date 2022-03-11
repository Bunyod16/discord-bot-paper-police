from tabnanny import check
from discord.ext import commands, tasks
from blockchain_utils import check_ownership, check_tx
from utils import get_token, VERIFY_CHANNEL_ID, POLICY_ID, GUILD_ID, NFT_ATTRIBUTES, WHALE_REQ, tz
from commands import general_commands
from api_firestore import get_tx, delete_tx, generate_tx, add_holder, delete_holder, get_all_holders, get_all_tx
import messages
import discord
import revoke_roles
from datetime import datetime, timezone
import math

PREFIX = ("~")
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=PREFIX, description='Hi', help_command=None, intents=intents)

@bot.command()
async def verify(message):
    if (message.channel.id != int(VERIFY_CHANNEL_ID)):
        print("used in the wrong channel")
        return
    user = await bot.fetch_user(message.author.id)
    if (not get_tx(message.author.id)):
        amount = generate_tx(message.author.id)
        await user.send(messages.start_instructions(message.author,amount))
    else:
        await user.send(messages.on_going_tx(message.author))

@bot.command()
async def help(message):
        await message.channel.send(embed=messages.help_message())

async def assign_roles(data, user, addr, num):
    guild = bot.get_guild(GUILD_ID)
    burning_head = guild.get_role(941898769526571079)
    golden_head = guild.get_role(941898593051226113)
    whale_role = guild.get_role(941898684201832559)
    phc_holder_role = guild.get_role(950982464678002730)
    await user.add_roles(phc_holder_role)
    if (num >= WHALE_REQ):
        await user.add_roles(whale_role)
    
    if (data == "Burning Head"):
        await user.add_roles(burning_head)

    if (data == "Golden Head"):
        await user.add_roles(golden_head)
    delete_tx(user.id)
    add_holder(user.id, addr)

async def give_roles(user, addr):
    nfts = check_ownership(addr, POLICY_ID)
    if (nfts == 0):
        return
    print(nfts)
    num = len(nfts)
    for nft in nfts:
        if (nft["Head"] in NFT_ATTRIBUTES):
            await assign_roles(nft["Head"], user, addr, num)

@bot.command()
async def tx(message, *args):
        if (message.channel.id != int(VERIFY_CHANNEL_ID)):
            await message.reply("Please use this command in the `#wallet-verification` channel.")
            return
        if (len(args) != 1):
            await message.reply("Please provide your transaction hash, example `~tx 41nfa91u24bacml148gakf9391nd`")
            return
        if (get_tx(message.author.id) == 0):
            await message.reply("You have not initiated a verification yet, please head over to the verification channel in the Paper Head Club.")
            return
        amount = float(get_tx(message.author.id)["tx_amount"])
        info = check_tx(args[0], amount)
        if (info["status"] == 1):
            await message.reply(messages.success_status())
            await give_roles(message.author,info["addr"])
            await message.message.delete()
        elif (info["status"] == 0):
            await message.reply(messages.wrong_amount_status())
        else:
            await message.reply(messages.failed_status())

@bot.command(pass_context = True)
async def clear(ctx, number):
  if (ctx.author.id == 237063450646282241):
      mgs = [] #Empty list to put all the messages in the log
      number = int(number) #Converting the amount of messages to delete to an integer
      async for x in ctx.message.channel.history(limit = number):
        await x.delete()
      print(mgs)

async def check_current_holders():
    holders = get_all_holders()
    guild = bot.get_guild(GUILD_ID)
    holder_dct = {}
    for holder in holders:
        holder = holder.to_dict()
        holder_dct[holder["user_id"]] = holder["addr"]
    for member in guild.members:
        if str(member.id) in holder_dct.keys():
            nfts = check_ownership(holder_dct[str(member.id)], POLICY_ID)
            if (len(nfts) == 0):
                print("doesnt have nfts")
                await revoke_roles.revoke_all_roles(member, bot)
            else:
                await revoke_roles.check_whale(member, nfts, bot)
                await revoke_roles.check_ghead(member, nfts, bot)
                await revoke_roles.check_bhead(member, nfts, bot)
            for role in member.roles:
                has_holder_role = 0
                if role.id in [941898769526571079, 941898593051226113, 941898684201832559]:
                    has_holder_role = 1
                if (has_holder_role == 0):
                    delete_holder(member.id)

def get_remaining_time(info):
    current_time = datetime.now(tz=timezone.utc)
    target_time = datetime.strptime(
			info, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
    difference =(target_time - current_time)
    seconds = difference.total_seconds()
    minutes = seconds / 60
    hours = math.floor(minutes / 60)
    minutes = math.floor(minutes - (hours * 60))
    days = math.floor(hours / 24)
    if (days >= 1):
        hours += (days * 24)
    if (hours < 0 or minutes < 0):
        hours = 0
        minutes = 0
    return ({"hours":hours,"minutes":minutes})

async def delete_old_tx():
    txs = get_all_tx()
    for tx in txs:
        tx = tx.to_dict()
        time = str(tx["time"])[:16]
        remaining = get_remaining_time(time)
        print(remaining)
        if (remaining["hours"] == 0 and remaining["minutes"] == 0):
            delete_tx(tx["user_id"])


@bot.event
async def on_ready():
    global mention_string
    global SERVER_ID
    global MENTION_ROLE_NAMES

    print(bot.user.name, "is online")
    print(bot.user.id)
    timed_checker.start()


@tasks.loop(hours=3)
async def timed_checker():
  print("Timed job started")
  await check_current_holders()
  await delete_old_tx()


bot.add_cog(general_commands())
bot.run(get_token())