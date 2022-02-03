
import os
import discord
from discord.ext import commands
from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException
from substrateinterface.utils.ss58 import ss58_encode
from dotenv import load_dotenv
load_dotenv()
# Your Discord bot token
faucet_mnemonic =os.getenv('MNEMONIC')
bot = commands.Bot(command_prefix='!')
mnemonic = Keypair.generate_mnemonic()
keypair = Keypair.create_from_mnemonic(faucet_mnemonic)
# substrate RPC node
node_rpc = "http://127.0.0.1:9933"

@bot.command(name='send', help='Send token from faucet')
async def nine_nine(ctx, arg):
    if (ctx.channel.type == "private"):
        # Forbid DM in discord
        await ctx.send("Hold on Capt'ain, you can't send me private messages !")
    else:
        substrate = SubstrateInterface(
            url=node_rpc,
            ss58_format=42,
            type_registry_preset='substrate-node-template'
        )
        call = substrate.compose_call(
        call_module='Balances',
        call_function='transfer',
        call_params={
            'dest': arg,
            'value': 1 * 10**12
            }
        )   
        reply = ""
        extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)
        reply = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=False)
        await ctx.send(ctx.author.mention + " Awesome, you just received 100 dPIRL, it has no real value it's only the testnet token :) " +  reply['extrinsic_hash'] + str(ctx.channel.type))

bot.run(os.getenv('TOKEN'))