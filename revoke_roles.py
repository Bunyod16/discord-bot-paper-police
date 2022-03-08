from utils import HOLDER_ROLE_IDS, WHALE_REQ, GUILD_ID

ROLE_WHALE = 941898684201832559
ROLE_GOLDEN = 941898593051226113
ROLE_BURNING = 941898769526571079

async def revoke_all_holder_roles(user, bot):
    guild = bot.get_guild(GUILD_ID)
    for role_id in HOLDER_ROLE_IDS:
        role = guild.get_role(role_id)
        await user.remove_roles(role)
    print(f"revoked all holder roles from {user}")

async def check_whale(user, nfts, bot):
    guild = bot.get_guild(GUILD_ID)
    whale_role = guild.get_role(941898684201832559)
    if (len(nfts) < WHALE_REQ):
        await user.remove_roles(whale_role)
        print(f"revoked whale role from {user}")

async def check_ghead(user, nfts, bot):
    guild = bot.get_guild(GUILD_ID)
    golden_head = guild.get_role(941898593051226113)
    check = 0
    for nft in nfts:
        try:
            if (nft["Head"] == "Golden Head"):
                check = 1
        except:
            print("no attribute head")
    if (check == 0):
        await user.remove_roles(golden_head)
        print(f"revoked golden head role from {user}")

async def check_bhead(user, nfts, bot):
    guild = bot.get_guild(GUILD_ID)
    burning_head = guild.get_role(941898769526571079)
    check = 0
    for nft in nfts:
        try:
            if (nft["Head"] == "Burning Head"):
                check = 1
        except:
            print("no attribute head")
    if (check == 0):
        await user.remove_roles(burning_head)
        print(f"revoked burning head role from {user}")
