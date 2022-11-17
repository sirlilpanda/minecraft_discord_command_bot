import json
import discord
from os import system
from discord.ext import commands
from discord.ext.commands import Context
from discord.role import Role
from typing import Callable, Any
from loadenv import load_env

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
BOT = commands.Bot(command_prefix='!', intents=intents)

with open("role_access.json", "r+") as txt:
    roles_accesses : dict = json.load(txt)

COMMAND = "screen -S {screen_name} -X stuff \"{command}\n\"",

@BOT.event
async def on_ready(): print(f'We have logged in as {BOT.user}')



@BOT.command()
async def minecraft(ctx, *args):
    """ """
    match args:
        case ("whitelist", server_name, name, *_):
            await parse_command(
                ctx, 
                ctx.author.id, 
                server_name, 
                "whitelist", 
                whitelist, 
                server_name, 
                name,
                on_complete_message=f"{name} has been whitelisted on server: {server_name}",
                on_fail_message=f"insufficient access"
            )

        case ("kick", server_name, name, *message):
            await parse_command(
                ctx, 
                ctx.author.id, 
                server_name, 
                "kick", 
                kick, 
                server_name, 
                name,
                message,
                on_complete_message=f"{name} has been kicked on server: {server_name}",
                on_fail_message=f"insufficient access"
            )
        
        case ("restart", server_name, *_):
            await parse_command(
                ctx, 
                ctx.author.id, 
                server_name, 
                "restart", 
                restart, 
                server_name, 
                on_complete_message=f"{server_name} has been restarted",
                on_fail_message=f"insufficient access"
            )

async def parse_command(ctx: Context, auth_id: int, server_name: str, command_name: str, command_func: Callable, *command_args: tuple[Any, ...], on_complete_message: str = "worked", on_auth_fail_message: str = "failed", check_access = True) -> None:
    print(command_args)
    if check_access:
        auth_id = ctx.author.id
        roles : list[Role] = (await ctx.guild.fetch_member(auth_id)).roles
        if (check_command_access(roles, command_name) and check_server_access(roles, server_name)):
            command_func(*command_args)
            await ctx.send(on_complete_message)
        else:
            await ctx.send(on_auth_fail_message)
    else:
        command_func(*command_args)

def check_command_access(author_roles : list[Role], command_name: str) -> bool:
    for i in _find_role(author_roles):
        if i["COMMANDS"][command_name]:
            return True
    return False

def check_server_access(author_roles, server_name: str) -> bool:
    for i in _find_role(author_roles):
        if server_name in i["SERVERS"]:
            return True
    return False

def _find_role(author_roles):
    for author_role in author_roles:
        for roles_role_id, roles_state in roles_accesses["ROLES"].items():
            if str(author_role.id) == roles_role_id:
                yield roles_state

def send_command(screen_name: str, command: str) -> None:
    system(
        COMMAND.format(
            screen_name=screen_name, 
            command=f"{command}"
        )
    )
    
def whitelist(server_name: str, name: str) -> None:
    send_command(server_name, f"/whitelist add {name}")

def restart(server_name: str) -> None:
    send_command(server_name, f"/stop")
    send_command(server_name, f"./run")

def kick(server_name: str, name: str, message: str) -> None:
    send_command(server_name, f"/kick {name} {' '.join(message)}")

def main():
    BOT.run(load_env(".env")["TOKEN"])

if __name__ == "__main__":
    main()