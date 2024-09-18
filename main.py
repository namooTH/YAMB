import discord
from discord.ext import commands
import os
import logging
import asyncio
import yaml
import sqlite3
import psutil
import sys
import wavelink
from colorama import Back, init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Custom logging format using colorama
class CustomFormatter(logging.Formatter):
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: Fore.WHITE + format + Style.RESET_ALL,
        logging.INFO: Fore.CYAN + format + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + format + Style.RESET_ALL,
        logging.ERROR: Fore.RED + format + Style.RESET_ALL,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + format + Style.RESET_ALL,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.format)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Configure the logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Define a custom credits function
def log_credits(message):
    logger.info(Fore.BLACK + Back.WHITE + message + Style.RESET_ALL)

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        command_prefix = '!'
        super().__init__(command_prefix=command_prefix, intents=intents)

        # Get bot token from file
        try:
            with open("token.yml", "r") as file:
                self.token = file.readline().strip()
        except FileNotFoundError:
            logger.critical("Token file not found. Please ensure 'token.yml' exists.")
            sys.exit(1)

        self.cogsfolder = "cogs"

        # Database connection
        try:
            self.quote_db = sqlite3.connect("quote.db")
            logger.info("Connected to the SQLite database.")
        except sqlite3.Error as e:
            logger.critical(f"Database connection failed: {e}")
            sys.exit(1)

        # Persistent variables
        self.music_queue = {}

    async def load_extensions(self):
        log_credits("EnhancedInit written by razrblds for Namaku")
        log_credits("Currently using V1.5")
        log_credits("This is made for YAMB and YAMB only. If you need a version for yourself, ask the contributor.")
        logger.info("Loading cogs...")

        for file in os.listdir(self.cogsfolder):
            if file.endswith(".py"):
                cog_name = f"{self.cogsfolder}.{file[:-3]}"
                await self._load_cog(cog_name)

        logger.info("All cogs loaded successfully.")

    async def _load_cog(self, cog_name):
        try:
            await self.load_extension(cog_name)
            logger.info(f"Loaded {cog_name} cog.")
        except Exception as e:
            logger.error(f"Failed to load cog {cog_name}: {e}")

    async def parse_args(self, args, prefix):
        action = args[len(prefix) + 1:].split(">")
        errors = []
        actions = []
        for a in action:
            root_action = ""
            child_action = None
            is_assigned = False
            rawaction = a
            while len(rawaction) > 0:
                match rawaction[0]:
                    case "=":
                        is_assigned = True
                    case _:
                        additional_info = ""
                        if is_assigned:
                            try:
                                child_action = yaml.safe_load(rawaction)
                                break
                            except Exception as e:
                                additional_info = f"\n```{e}```"
                                errors.append((f"Invalid action at `{rawaction}`{additional_info}"))
                                break
                        root_action += rawaction[0]
                rawaction = rawaction[1:]
            actions.append({root_action: child_action})
        return [actions, errors]

    #async def setupwavelink(self):
    #    node: wavelink.Node = wavelink.Node(uri='http://localhost:2333', password='youshallnotpass')
    #    await wavelink.Pool.connect(client=self, nodes=[node])

    async def initialization_check(self):
        logger.info("Starting initialization check...")

        # Check CPU and RAM usage
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()

        logger.info(f"CPU Usage: {cpu_usage}%")
        logger.info(f"Memory Usage: {memory_info.percent}%")
        logger.info(f"Total RAM: {memory_info.total / (1024 ** 3):.2f} GB")
        logger.info(f"Available RAM: {memory_info.available / (1024 ** 3):.2f} GB")

        # Check database connection
        try:
            self.quote_db.execute("SELECT 1")
            logger.info("Database connection: OK")
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            sys.exit(1)

        logger.info("Initialization check completed successfully.")

    async def periodic_system_check(self):
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()

            logger.info(f"Periodic Check - CPU Usage: {cpu_usage}%")
            logger.info(f"Periodic Check - Memory Usage: {memory_info.percent}%")
            logger.info(f"Periodic Check - Total RAM: {memory_info.total / (1024 ** 3):.2f} GB")
            logger.info(f"Periodic Check - Available RAM: {memory_info.available / (1024 ** 3):.2f} GB")

            await asyncio.sleep(120)  # Wait for 2 minutes

bot = Bot()

@bot.command()
async def reload(ctx, cog):
    if ctx.author.id == 899113384660844634:  # Replace with your own ID
        try:
            await bot.reload_extension(f"{bot.cogsfolder}.{cog}")
            await ctx.send(f"Reloaded {cog}")
            logger.info(f"{cog} cog reloaded by {ctx.author.name}.")
        except Exception as e:
            await ctx.send(f"Failed to reload {cog}")
            logger.error(f"Failed to reload cog {cog}: {e}")

@bot.command()
async def sync(ctx):
    if ctx.author.id == 899113384660844634:  # Replace with your own ID
        try:
            synced = await bot.tree.sync()
            await ctx.send(f"Synced {len(synced)} command(s).")
            logger.info(f"Commands synced by {ctx.author.name}.")
        except Exception as e:
            await ctx.send("Failed to sync commands.")
            logger.error(f"Failed to sync commands: {e}")

@bot.listen()
async def on_ready():
    logger.info(f"Logged in as {bot.user}")

async def main():
    async with bot:
        await bot.initialization_check()  # Perform the initialization check
        asyncio.create_task(bot.periodic_system_check())  # Start the periodic system check
        await bot.load_extensions()
        #await bot.setupwavelink()
        await bot.start(bot.token)

asyncio.run(main())
