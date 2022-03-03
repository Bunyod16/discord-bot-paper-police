import requests
from bs4 import BeautifulSoup
from blockfrost import BlockFrostApi, ApiError, ApiUrls

def find_stake(addr):
    r = requests.get(f"https://cardanoscan.io/address/{addr}")
    soup = BeautifulSoup(r.content, "html.parser")
    res = soup.find_all("span", {"class":"text-muted"})
    stake_addr = res[1].text
    if (stake_addr.startswith("stake")):
        return (stake_addr)
    return (0)

def init_api():
    api = BlockFrostApi(
        project_id='mainnetqgaytYOBu3vLFgDCcNM2ujE6gx4igY9i',
        base_url=ApiUrls.mainnet.value,
    )
    return (api)

def check_ownership(addr, policy_id):
    api = init_api()
    stake_address = find_stake(addr)
    assets = api.account_addresses_assets(stake_address=stake_address)
    ret = []
    for asset in assets:
        js = asset.to_dict()
        if (js["unit"].startswith(policy_id)):
            info = api.asset(js["unit"]).to_dict()
            ret.append(info["onchain_metadata"].to_dict())
    if (len(ret) != 0):
        return(ret)
    return (0)

def check_tx(tx_id, amount):
    try:
        api = init_api()
        info = api.transaction_utxos(tx_id)
        outputs = info.outputs
        inputs = info.inputs
        for output in outputs:
            lovelace = int(output.amount[0].quantity)
            ada = lovelace / 1000000
            if (ada == amount):
                return ({"status":1,"addr":inputs[0].address})
    except Exception as err:
        print(err)
        return ({"status": -1})
    return ({"status": 0})
        