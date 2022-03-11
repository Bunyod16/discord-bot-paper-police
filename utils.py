import os
from dateutil import tz
from datetime import datetime

tzstr = "UTC"
tz = tz.gettz(tzstr)

def now():
  return datetime.now(tz)

CURRENT_COLLECTION="current"
HOLDER_COLLECTION="holder"
VERIFY_CHANNEL_ID = "948963308717867098"
ADMINS = []
HOLDER_ROLE_IDS = [941898769526571079,941898593051226113,941898684201832559,950982464678002730]
DATA_TO_ROLES = [{"burning head":[948925028278366249]},]
POLICY_ID = "a0e859a7b29dbfc2b798ed720802fff406fe09b8e3c9a6b3affb7320"
GUILD_ID = 918510660126638080
NFT_ATTRIBUTES = ["Golden Head", "Burning Head"]
WHALE_REQ = 14

def is_admin(id):
    if (id in ADMINS):
        return (1)
    return (0)

def get_token():
    return (os.environ["TOKEN"])