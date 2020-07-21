from crud.item_db import item_db_id_list
from crud.discord import insert_discord_request, return_discord_wishlist, delete_discord_list, delete_discord_item
from discord.ext import commands, tasks
from request_keys import discord_key
from controler.checker import checker
import asyncio

id_list = item_db_id_list()


client = commands.Bot(command_prefix='!')


@tasks.loop(seconds=6000)
async def my_loop():
    await checker()


@client.event
async def on_ready():
    print("BOT Online.")


async def reply(item_id: int, item_name: str, price: int, stores: str, discord_user: int):
    user = await client.get_user_info(str(discord_user))
    await client.send_message(user, f"Item: {item_id} - {item_name} is selling for: {price}\n {stores}")


@client.command()
async def buy(ctx, item_id: int, *, price: int):
    if item_id in id_list:
        insert_discord_request(item_id, price, ctx.message.author.id)
        await ctx.author.send(F" Added: item: {item_id}, price limit: {price}")

    else:
        await ctx.send(F" The item_id isn't valid.")


@buy.error
async def buy_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('This comand needs 2 numerical parameters: item_id price.  Use just numbers: Ex: 509 800.')


@client.command()
async def list(ctx):
    player_list = return_discord_wishlist(ctx.message.author.id)
    if len(player_list) == 0:
        await ctx.author.send("List is empty")
    else:
        for lista in player_list:
            await ctx.author.send(F"""Item_ID: {lista[0]}, Item_Name: {lista[1]}, Target_Price: {lista[2]}""")


@list.error
async def list_erro(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.author.send('There is no need to any extra argumento on !list')


@client.command()
async def clear(ctx):
    delete_discord_list(ctx.message.author.id)
    await ctx.author.send('Done! List is empty. ')


@clear.error
async def clear_erro(ctx, error):
    pass


@client.command()
async def delete(ctx, *args):
    discord_id = ctx.message.author.id
    for item in args:
        try:
            item = int(item)
            delete_discord_item(discord_id, item)
            await ctx.author.send(f" Item: {item} deleted.")
        except ValueError:
            pass


@delete.erro
async def clear_erro(ctx, error):
    pass


@client.command()
async def commands(ctx):
    await ctx.send("""!buy item\_ID price -> Add a item to your wishlist. Use just numbers spaces or underlines \n
\\\\Ex: !Buy 509 6000 or !buy 509 6\_000 \n\n!list -> Will return your wishlist \n\n!cleare -> Will DELETE all itens\
\\\\ from your wishlist \n\n!delete item\_id -> Will delete the desired item from your wishlist""")


@commands.erro
async def comands_erro(ctx, error):
    pass


client.run(discord_key)

