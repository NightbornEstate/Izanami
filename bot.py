# This file was created by codingJWilliams

from discord.ext import commands

description = '''Nightborn's welcomer bot'''

# this specifies what extensions to load when the bot starts up
startup_extensions = ["welcome"]

bot = commands.Bot(command_prefix='.', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_member_join(member):
    await bot.cogs['Welcome'].setup_welcome(member)

def is_owner(ctx):
    return ctx.message.author.id == "193053876692189184"

@bot.command(pass_context=True)
@commands.check(is_owner)
async def wel(ctx):
  """Welcomes a member"""
  await bot.cogs['Welcome'].setup_welcome(ctx.message.author, ctx.message.channel.id)

@bot.command()
@commands.check(is_owner)
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command()
@commands.check(is_owner)
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    with open("token.txt") as f:
      bot.run(f.read().replace("\n", ""))