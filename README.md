# Discord Bot - Mały Warchlak

## Description

Mały Warchlak is a Discord bot written in Python using the Discord.py library. The bot is designed to provide entertainment features, including meme generation, joke retrieval, and keyword responses.

## Features

- **Meme Generation**: `!mem` Generate memes for a touch of humor.
- **Joke Retrieval**: `!joke` Enjoy jokes fetched by the bot.
- **Funny quotes**: `!boner` or `!bomba` Enjoy jokes fetched by the bot.
- **Keyword Responses**: Get predefined messages in response to specific keywords.
- **OpenAI's responses**: The bot leverages the power of OpenAI to enhance its conversation capabilities and provide more engaging and intelligent responses.
- **Modular Design**: Implementation is based on Discord.py cogs for easy maintenance.
- **Additional Admin Tools**: Check the section below for new admin tools for data backup and word counting.

## Usage

To use the bot, follow these steps:

1. Clone the repository to your local machine.
2. Install dependencies using `pip install -r requirements.txt`.
3. Set up your Discord bot token in the `.env` file.
4. Run the main file, typically named `main.py`.

## Configuration

- Customize meme generation by selecting categories or sources.
- Adjust the number of available jokes or specify a source for joke retrieval.
- Define keyword responses in the `keyword_responses.txt` file.

## OpenAI Conversation
To engage in a conversation with the bot using OpenAI, mention the bot and provide your message. The bot will respond with an intelligent reply.

## Music Playback

Enjoy your favorite tunes with Mały Warchlak. Use the following commands in a voice channel:

- `!wbijaj`: Bot joins the voice channel.
- `!wyjdz`: Bot leaves the voice channel.
- `!graj <url>`: Bot plays music from the provided URL.
- `!stop`: Bot stops playing music.

## Admin Tools

### Backup Messages from Channels
This tool allows you to back up messages from selected channels. All messages are saved to a text file, and the most frequently occurring words are calculated.
Usage: `!mapuj <channel_id>`
### Finding Most Popular Words in a Backup
This tool helps find the most popular words in a backup of messages.
Usage: `!find <file_name> <number>`

### Dynamic Reaction Control
You can dynamically control the bot's reactions to user events by adjusting its activity state:

- **Sleep Mode**: Temporarily disables the bot's reaction to user messages.
- **Wake Up Mode**: Re-enables the bot's reaction to user messages.

This dynamic control allows you to manage the bot's activity without the need for specific commands, providing flexibility in its responsiveness.


## License

This project is open source and available under the [MIT License](LICENSE).

## Author

Kraverek

Feel free to contribute, report issues, or suggest improvements!