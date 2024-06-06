import discord
from discord.ext import commands, tasks
import re
from collections import defaultdict
from pymongo import MongoClient
import logging

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

MONGO_URI = ''
DB_NAME = ''
COLLECTION_NAME = ''

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Channel IDs
GLOBAL_LOGS_CHANNEL_ID = 1246568909784482004
LEADERBOARD_CHANNEL_ID = 1247287177419685968

hits_count = defaultdict(int)

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user}')
    update_leaderboard.start()

async def count_hits():
    hits_count.clear()  
    channel = bot.get_channel(GLOBAL_LOGS_CHANNEL_ID)
    async for message in channel.history(limit=100):  
        if message.embeds:  
            for embed in message.embeds:
                if "An account was Converted By" in embed.description:
                    user_match = re.search(r'By <@!?(\d+)>', embed.description)
                    if user_match:
                        mentioned_user_id = user_match.group(1)
                        hits_count[mentioned_user_id] += 1

def update_database():
    for user, count in hits_count.items():
        collection.update_one(
            {'user': user},
            {'$inc': {'hits': count}},
            upsert=True
        )

async def create_leaderboard_embed():
    sorted_hits = collection.find().sort('hits', -1)
    leaderboard = discord.Embed(
        title="Xtract Converter - Leaderboard",
        description="Top users based on the number of hits.",
        color=discord.Color.blue()
    )
    leaderboard.set_footer(text="Leaderboard updated")

    for i, entry in enumerate(sorted_hits, start=1):
        if 'user' in entry:
            user_id = entry['user']
            hits = entry.get('hits', 0)  
            user_name = await get_user_name(user_id)
            leaderboard.add_field(
                name=f"{i}. {user_name}",
                value=f"Hits: {hits}",
                inline=False
            )
        else:
            logging.warning(f"Missing 'user' field in database entry: {entry}")

    return leaderboard

async def get_user_name(user_id):
    user = await bot.fetch_user(int(user_id))
    return user.name

async def send_leaderboard():
    leaderboard = await create_leaderboard_embed()
    leaderboard_channel = bot.get_channel(LEADERBOARD_CHANNEL_ID)
    message = await leaderboard_channel.send(embed=leaderboard)
    
    collection.update_one(
        {'type': 'leaderboard_message'},
        {'$set': {'message_id': message.id}},
        upsert=True
    )

async def edit_leaderboard():
    leaderboard = await create_leaderboard_embed()
    leaderboard_channel = bot.get_channel(LEADERBOARD_CHANNEL_ID)
    message_data = collection.find_one({'type': 'leaderboard_message'})
    if message_data:
        message_id = message_data['message_id']
        message = await leaderboard_channel.fetch_message(message_id)
        await message.edit(embed=leaderboard)
    else:
        message = await leaderboard_channel.send(embed=leaderboard)
        collection.update_one(
            {'type': 'leaderboard_message'},
            {'$set': {'message_id': message.id}},
            upsert=True
        )

@tasks.loop(minutes=10)
async def update_leaderboard():
    await count_hits()
    update_database()
    await edit_leaderboard()

@update_leaderboard.before_loop
async def before_update_leaderboard():
    await bot.wait_until_ready() 
print(f"DIOR WAS HERE")
bot.run('')
