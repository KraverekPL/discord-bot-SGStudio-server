# Discord Bot - Mały Warchlak

## Description

Mały Warchlak is a Discord bot written in Python using the Discord.py library. The bot is designed to provide entertainment features, including meme generation, joke retrieval, and keyword responses.

## Features

- **Meme Generation**: Generate memes for a touch of humor.
- **Joke Retrieval**: Enjoy jokes fetched by the bot.
- **Keyword Responses**: Get predefined messages in response to specific keywords.
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

## Admin Tools

### Backup Messages from Channels
This tool allows you to back up messages from selected channels. All messages are saved to a text file, and the most frequently occurring words are calculated.

### Finding Most Popular Words in a Backup
This tool helps find the most popular words in a backup of messages.

### Dynamic Reaction Control
You can dynamically control the bot's reactions to user events by adjusting its activity state:

- **Sleep Mode**: Temporarily disables the bot's reaction to user messages.
- **Wake Up Mode**: Re-enables the bot's reaction to user messages.

This dynamic control allows you to manage the bot's activity without the need for specific commands, providing flexibility in its responsiveness.


## License

This project is open source and available under the [MIT License](LICENSE).

## Future Implementations

Here are some planned features and improvements for Mały Warchlak:

- Display quotes from Captain Bomba and the Bonner cartoon.
- Implement image generation features.
- Add a simple gambling game.
- Enable music playback on a voice channel.

## Author

Kraverek

Feel free to contribute, report issues, or suggest improvements!