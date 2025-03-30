from discord_bot import bot
import os
from dotenv import load_dotenv
load_dotenv()

# Execute bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))