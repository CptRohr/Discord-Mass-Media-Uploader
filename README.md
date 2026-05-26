# Discord Media Uploader

Discord Media Uploader is a small Python Discord bot that uploads files from a local `media` folder to the Discord channel where you run a command.

Use it when you have a batch of images, videos, documents, or other files that you want to send without manually attaching them one by one.

## What It Does

- Uploads files from the `media` folder when you run `!kaboom`.
- Sends files in batches of up to 10 attachments per Discord message.
- Skips files that are already listed in `logs.log`.
- Can resend everything with `!kaboom all`.
- Can reset upload history with `!kaboom reset`.
- Moves files Discord rejects as too large into the `large` folder.
- Ignores hidden files such as `.gitkeep`.

The bot does not automatically watch the folder. It only uploads when you run a command in Discord.

## Requirements

- Python 3.8 or newer
- A Discord bot token
- The bot invited to your Discord server
- Discord bot permissions:
  - View Channels
  - Send Messages
  - Attach Files
  - Read Message History
- Message Content Intent enabled in the Discord Developer Portal

See [bottutorial.md](./bottutorial.md) if you need help creating and inviting the bot.

## Quick Start

1. Clone or download this repository.

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create and invite your Discord bot.

Follow [bottutorial.md](./bottutorial.md), then copy your bot token.

4. Set your bot token.

For a temporary PowerShell session:

```powershell
$env:DISCORD_BOT_TOKEN = "your-bot-token-here"
```

For a persistent Windows user environment variable:

```powershell
setx DISCORD_BOT_TOKEN "your-bot-token-here"
```

After using `setx`, close and reopen PowerShell. If you run the bot from VS Code, restart VS Code too.

To confirm the current PowerShell can see the token:

```powershell
echo $env:DISCORD_BOT_TOKEN
```

If that prints nothing, the bot will ask for the token when it starts.

5. Put your files in the `media` folder.

6. Start the bot:

```bash
python DiscordMediaUploader.py
```

7. In Discord, go to the channel where you want the files uploaded and run:

```text
!kaboom
```

## Commands

### `!kaboom`

Uploads files from `media` that are not already listed in `logs.log`.

Use this for normal uploads. Files are sent in batches of up to 10 attachments per message.

Batching works like this:

- The bot collects all uploadable files.
- It splits them into groups of up to 10 files.
- It tries to send each group as one Discord message.
- If a batch fails, the bot retries that group one file at a time.

This means uploads may sometimes appear as one message with multiple files, and sometimes as separate messages. Separate messages usually mean Discord rejected the batch because of file size, total attachment size, file type, rate limits, or a temporary API issue.

### `!kaboom all`

Uploads every file currently in `media`, even if it already appears in `logs.log`.

Use this when you want to resend files.

### `!kaboom reset`

Clears the upload history in `logs.log`.

After this, `!kaboom` will treat files in `media` as new again.

## Token Safety

Never paste your real bot token into:

- `config.py`
- GitHub commits
- Discord messages
- Screenshots
- README files

This project reads the token from the `DISCORD_BOT_TOKEN` environment variable:

```python
TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
```

The included `config.py` is safe to commit because it does not contain a real token.

If your token is ever exposed, reset it immediately in the Discord Developer Portal.

You can use a local `.env` file with your own workflow if you prefer. `.env` files are ignored by Git in this project, but do not upload them manually to GitHub.

## Project Folders

### `media`

Put files here before running `!kaboom`.

Files beginning with `.` are ignored by the bot. The `.gitkeep` file only exists so GitHub keeps the folder in the repository.

### `large`

Files that Discord rejects as too large are moved here.

### `logs.log`

The bot creates this file when it starts. It records uploaded files so the bot can skip duplicates later.

If `!kaboom` says there are no remaining files, every uploadable file in `media` is probably already listed in `logs.log`.

To resend them:

```text
!kaboom all
```

To clear upload history first:

```text
!kaboom reset
!kaboom
```

## Troubleshooting

### The bot asks for my token even after using `setx`

`setx` only affects new terminals and newly opened apps.

Close and reopen PowerShell, then check:

```powershell
echo $env:DISCORD_BOT_TOKEN
```

If you run the bot from VS Code, restart VS Code too.

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

### `.gitkeep` was uploaded

Update to the latest version of this project. The bot now ignores files beginning with `.`.

### A file is not uploaded

The file may be too large for Discord. Check the `large` folder and the console output.

If a batch fails, the bot retries those files one by one. This helps it find the specific file that failed without stopping the whole upload.

## GitHub Notes

The following are ignored by Git:

- `media/*`
- `large/*`
- `logs.log`
- `.env`
- `.venv`
- `__pycache__`

Do not manually upload private media files, `.env` files, or real tokens through GitHub's website.

## License

This project is licensed under the [MIT License](LICENSE).

## Credits

Original project by [Nikhil-Makwana1](https://github.com/Nikhil-Makwana1/DiscordMediaUploader).

Modified by [CptRohr](https://github.com/CptRohr).
