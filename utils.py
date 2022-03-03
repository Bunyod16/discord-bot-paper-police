from audioop import add
import os

CURRENT_COLLECTION="current"
HOLDER_COLLECTION="holder"
VERIFY_CHANNEL_ID = "948963308717867098"
ADMINS = []
DATA_TO_ROLES = [{"burning head":[948925028278366249]},]
POLICY_ID = "a0e859a7b29dbfc2b798ed720802fff406fe09b8e3c9a6b3affb7320"
GUILD_ID = 918510660126638080
NFT_ATTRIBUTES = ["Golden Head", "Burning Head"]

def is_admin(id):
    if (id in ADMINS):
        return (1)
    return (0)

def get_token():
    return (os.environ["TOKEN"])