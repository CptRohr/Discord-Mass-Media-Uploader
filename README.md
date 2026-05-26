# Discord Media Uploader

Discord Media Uploader is a small Python Discord bot for uploading every file in a local `media` folder to the Discord channel where you run a command.

It is useful when you have a batch of images, videos, documents, or other files that you want to send to a server without manually attaching them one by one.

## How It Works

The bot does not watch the folder automatically. Instead, you run a Discord command when you are ready to upload.

- Put files inside the `media` folder.
- Start the bot.
- In Discord, type `!kaboom` in the channel where the files should be sent.
- The bot uploads files that have not already been recorded in `logs.log`.
- Files that are too large for Discord are moved to the `large` folder.

## Requirements

- Python 3.8 or newer
- A Discord bot token
- The bot must be invited to your server
- The bot needs permission to read messages, send messages, and attach files
- Message Content Intent must be enabled in the Discord Developer Portal

## Installation

1. Clone or download this repository.
2. Install the required Python package:

```bash
pip install -r requirements.txt
```

3. Create a Discord bot in the Discord Developer Portal.

See [bottutorial.md](./bottutorial.md) for a step-by-step guide.

4. Set your bot token as an environment variable.

PowerShell:

```powershell
$env:DISCORD_BOT_TOKEN = "your-bot-token-here"
```

Command Prompt:

```bat
set DISCORD_BOT_TOKEN=your-bot-token-here
```

Linux or macOS:

```bash
export DISCORD_BOT_TOKEN="your-bot-token-here"
```

The project also includes `config.example.py` to show how the token is loaded:

```python
TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
```

Keep this token private. If it is shared publicly, reset it immediately in the Discord Developer Portal.

5. Add your files to the `media` folder.

6. Start the bot:

```bash
python DiscordMediaUploader.py
```

## Discord Commands

Run these commands in the Discord channel where you want the files to be uploaded.

### `!kaboom`

Uploads files from the `media` folder that are not already listed in `logs.log`.

Use this for normal uploads. If a file was already uploaded before, the bot skips it so you do not accidentally post duplicates.

### `!kaboom all`

Uploads every file currently in the `media` folder, even if it already appears in `logs.log`.

Use this if you want to resend files.

### `!kaboom reset`

Clears the upload log.

After running this, `!kaboom` will treat the files in `media` as new again.

## Folders And Files

### `media`

Put files here before running the upload command.

### `large`

Files that Discord rejects as too large are moved here.

### `logs.log`

The bot creates this file when it starts and records uploaded files here. This is how it knows which files have already been sent.

If `!kaboom` says there are no remaining files, it usually means every file in `media` is already listed in `logs.log`.

You can either run:

```text
!kaboom all
```

or:

```text
!kaboom reset
!kaboom
```

## Troubleshooting

### The bot receives my command but sends nothing

Check whether the files are already listed in `logs.log`. If they are, the bot is skipping them to avoid duplicate uploads.

Use `!kaboom all` to resend them, or `!kaboom reset` to clear the upload history.

### The bot does not respond to commands

Make sure:

- The bot is online.
- The bot has access to the channel.
- Message Content Intent is enabled in the Discord Developer Portal.
- The bot has permission to read messages, send messages, and attach files.
- The command starts with `!`, for example `!kaboom`.

### A file is not uploaded

The file may be too large for Discord. Check the `large` folder and the console output.

## Notes

- Discord upload limits depend on the server and account level.
- The bot only uploads local files from the `media` folder.
- `media`, `large`, `logs.log`, `.env`, and virtual environments are ignored by Git.
- Do not commit real bot tokens to GitHub or share them in screenshots.

## License

This project is licensed under the [MIT License](LICENSE).
