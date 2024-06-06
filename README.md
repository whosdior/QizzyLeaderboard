# Xtract Converter Bot README

## Introduction
The Xtract Converter Bot is a Discord bot designed to track and display user activity through a leaderboard. It monitors messages in a specified channel for certain events, counts these events, and maintains a leaderboard to show the most active users. The bot uses MongoDB for data storage and leverages the `discord.py` library to interact with Discord.

## Features
- Monitors a specific Discord channel for messages containing certain keywords.
- Counts the occurrences of these messages for each user.
- Updates a leaderboard in a designated channel with the top users.
- Periodically updates the leaderboard every 10 minutes.

## Setup and Configuration

### Prerequisites
- Python 3.8+
- `discord.py` library
- `pymongo` library
- A MongoDB instance

### Installation
1. **Clone the Repository**:
   ```sh
   git clone [<repository-url>](https://github.com/whosdior/QizzyLeaderboard.git)
   cd QizzyLeaderboard
   ```

2. **Install Dependencies**:
   ```sh
   pip install discord.py pymongo
   ```

3. **Configure Environment Variables**:
   Create a `.env` file or configure the following variables in your environment:
   - `DISCORD_TOKEN`: Your Discord bot token.
   - `MONGO_URI`: URI for connecting to your MongoDB instance.
   - `DB_NAME`: Name of the database in MongoDB.
   - `COLLECTION_NAME`: Name of the collection in MongoDB.

4. **Update Channel IDs**:
   Modify the `GLOBAL_LOGS_CHANNEL_ID` and `LEADERBOARD_CHANNEL_ID` variables in the code to match your Discord server's channel IDs.

### Running the Bot
1. **Start the Bot**:
   ```sh
   python leaderboard.py
   ```

## Code Overview

### Libraries and Modules
- `discord`: Core library for interacting with Discord API.
- `discord.ext.commands`: Extension of `discord` for command handling.
- `discord.ext.tasks`: Extension of `discord` for background tasks.
- `re`: Regular expressions for parsing message content.
- `collections.defaultdict`: Data structure for counting occurrences.
- `pymongo`: MongoDB client for database operations.
- `logging`: For logging bot activities.

### Key Variables
- `MONGO_URI`: URI for MongoDB connection.
- `DB_NAME`: Database name.
- `COLLECTION_NAME`: Collection name.
- `GLOBAL_LOGS_CHANNEL_ID`: ID of the channel to monitor.
- `LEADERBOARD_CHANNEL_ID`: ID of the channel to post the leaderboard.

### Functions and Events
- `on_ready()`: Event handler for when the bot is ready.
- `count_hits()`: Counts the relevant messages in the specified channel.
- `update_database()`: Updates MongoDB with the counted data.
- `create_leaderboard_embed()`: Creates an embed object for the leaderboard.
- `get_user_name()`: Retrieves a user's name by their ID.
- `send_leaderboard()`: Sends a new leaderboard message.
- `edit_leaderboard()`: Edits the existing leaderboard message.
- `update_leaderboard()`: Task loop that periodically updates the leaderboard.

### Task Loop
The `update_leaderboard` task runs every 10 minutes, updating the hit counts and refreshing the leaderboard.

## Usage
- The bot will start counting messages in the specified channel once it's running.
- The leaderboard is updated every 10 minutes and posted/edited in the designated channel.
- Ensure the bot has the necessary permissions to read message history and send/edit messages in the specified channels.

## Logging
Logs are printed to the console with a basic configuration. Modify the `logging.basicConfig` call to customize logging as needed.

## Conclusion
The Xtract Converter Bot provides a simple way to track and display user activity in a Discord server through a dynamically updating leaderboard. Customize the bot's behavior by modifying the configuration variables and functions as needed.
