import discord

def help_message():
    title = "Paper Police Manual"
    description = ""
    fields = [
        {"name":"`~verify`", "description":"Initiate a verification request."},
        {"name":"`~tx tx_id`", "description":"Verify your wallet by making a small transaction."}
    ]
    message_help = discord.Embed(title=title, description=description, color=0x000000)
    for field in fields:
        message_help.add_field(name=field["name"], value=field["description"], inline=False)
    return (message_help)

def start_instructions(user, amount):
    message = f"Hi {user.name}, to verify that you own a Paper Head NFT please:\n\n1. Send **exactly {amount}** ADA from the wallet containing the NFT to any other wallet (can be one of your own wallets).\n\n2. Verify the transaction by using `~tx tx_id` in the #wallet-verification channel.\n\nFor example:\n `~tx f2a7ff69f1987017d791205f847f74ec2682f51dc186698483ac9ef17448505b`\n\n*you have 1 hour to verify your transaction"
    return (message)

def on_going_tx(author):
    message = f"Hi {author.name}, your verification status is: ON GOING"
    return (message)

def success_status():
    message = "✅ You have successfully confrimed your transaction, your roles will be given shortly!"
    return (message)

def failed_status():
    message = "❌ Failed to confirm the transaction, please make sure you copied the transaction id/hash correctly."
    return (message)

def wrong_amount_status():
    message = "❌ The transaction does not contain the correct amount of ADA transferred."
    return (message)