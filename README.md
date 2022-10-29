# Discord Music Bot

> This is a simple discord bot that can be added to any discord server.

## The main functionalities of the bot are:
1. A play command that takes a song name (e.g.: danger_zone.mp3) as argument. Invoking this command while present in a voice channel should cause the bot to connect to that channel and play the song. The song should be loaded from a local file(you can find some music in the folder called "muzica").
2. A list command that lists all available songs in the discord chat.
3. A scram command that tells the bot to disconnect from the current voice channel immediately.
4. An event handler for on_voice_state_update that checks if the bot was left alone in the channel after a user left. If the bot is indeed alone, it should also disconnect.

Feel free to download and maybe try putting it inside your server!
