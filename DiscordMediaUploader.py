import datetime
import os
import shutil
import discord
from discord.ext import commands
import config

LARGE_MEDIA = ""
CONTENT_FOLDER = ""
LOG_FILE = ""

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


def initialize():
    global CONTENT_FOLDER, LOG_FILE, LARGE_MEDIA

    current_dir = os.getcwd()
    content_dir = "media"
    large_dir = "large"

    CONTENT_FOLDER = os.path.join(current_dir, content_dir)
    LARGE_MEDIA = os.path.join(current_dir, large_dir)
    LOG_FILE = os.path.join(current_dir, "logs.log")

    prerequisite()


def prerequisite():
    if not os.path.exists(CONTENT_FOLDER):
        os.makedirs(CONTENT_FOLDER)

    if not os.path.exists(LARGE_MEDIA):
        os.makedirs(LARGE_MEDIA)

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as file:
            file.write("----------------------------------------\n")
            file.write("        Time           Size (MB)    Name\n")
            file.write("----------------------------------------\n")


def reset_log_file():
    with open(LOG_FILE, 'w') as file:
        file.write("----------------------------------------\n")
        file.write("        Time           Size (MB)    Name\n")
        file.write("----------------------------------------\n")


def uploaded_filenames():
    uploaded = set()

    with open(LOG_FILE, 'r') as file:
        for line in file:
            parts = line.rstrip().split(maxsplit=4)
            if len(parts) == 5:
                uploaded.add(parts[4])

    return uploaded


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    print("To start uploading, type !kaboom in the Discord channel")


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    print(f"Received message from {message.author}: {message.content}")
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    print(f"Command error: {getattr(ctx.command, 'name', None)} failed with: {error}")


@bot.command()
async def kaboom(ctx, mode: str = ""):
    print(f"kaboom command invoked by {ctx.author} in {ctx.channel}")
    channel = ctx.channel

    mode = mode.lower()
    upload_all = mode in ("all", "--all", "force", "--force")

    if mode in ("reset", "--reset"):
        reset_log_file()
        print("Upload log reset")
        await channel.send("Upload log reset. Run `!kaboom` to upload files again.")
        return

    if mode and not upload_all:
        await channel.send("Unknown option. Use `!kaboom`, `!kaboom all`, or `!kaboom reset`.")
        return

    logs = uploaded_filenames()
    uploaded_count = 0
    skipped_count = 0
    failed_count = 0

    with open(LOG_FILE, 'a') as file:
        for filename in os.listdir(CONTENT_FOLDER):
            file_path = os.path.join(CONTENT_FOLDER, filename)

            if not os.path.isfile(file_path):
                continue

            if not upload_all and filename in logs:
                skipped_count += 1
                continue

            try:
                filesize = os.path.getsize(file_path) / (1024 * 1024)
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                await channel.send(file=discord.File(file_path, filename))

                file.write(f"{current_time} {filesize:10.2f}    {filename}\n")
                uploaded_count += 1
                print(f"Uploaded: {current_time} {filesize:6.2f} MB  {filename}")

            except Exception as e:
                failed_count += 1

                if "Payload Too Large" in str(e):
                    large_file_path = os.path.join(LARGE_MEDIA, filename)
                    shutil.move(file_path, large_file_path)
                    print(f"Too large: {filename}")
                else:
                    print(f"Failed to upload {filename}: {e}")

    if uploaded_count:
        await channel.send(f"Uploaded {uploaded_count} file(s).")
    elif skipped_count:
        await channel.send("No remaining files to upload. Use `!kaboom all` to resend logged files or `!kaboom reset` to clear the upload log.")
        print("\nNo Remaining Files")
    else:
        await channel.send("No files found in the media folder.")
        print("\nNo Files Found")

    if failed_count:
        await channel.send(f"{failed_count} file(s) failed to upload. Check the console for details.")


def logo():
    line1 = "·▄▄▄▄  ▪  .▄▄ ·  ▄▄·       ▄▄▄  ·▄▄▄▄      • ▌ ▄ ·. ▄▄▄ .·▄▄▄▄  ▪   ▄▄▄·      ▐▄▄▄▄▄▄ .▄▄▄▄▄"
    line2 = "██▪ ██ ██ ▐█ ▀. ▐█ ▌▪▪     ▀▄ █·██▪ ██     ·██ ▐███▪▀▄.▀·██▪ ██ ██ ▐█ ▀█       ·██▀▄.▀·•██  "
    line3 = "▐█· ▐█▌▐█·▄▀▀▀█▄██ ▄▄ ▄█▀▄ ▐▀▀▄ ▐█· ▐█▌    ▐█ ▌▐▌▐█·▐▀▀▪▄▐█· ▐█▌▐█·▄█▀▀█     ▪▄ ██▐▀▀▪▄ ▐█.▪"
    line4 = "██. ██ ▐█▌▐█▄▪▐█▐███▌▐█▌.▐▌▐█•█▌██. ██     ██ ██▌▐█▌▐█▄▄▌██. ██ ▐█▌▐█ ▪▐▌    ▐▌▐█▌▐█▄▄▌ ▐█▌·"
    line5 = "▀▀▀▀▀• ▀▀▀ ▀▀▀▀ ·▀▀▀  ▀█▄▀▪.▀  ▀▀▀▀▀▀•     ▀▀  █▪▀▀▀ ▀▀▀ ▀▀▀▀▀• ▀▀▀ ▀  ▀      ▀▀▀• ▀▀▀  ▀▀▀ "
    information = "    ⭐️ Star the Repository  |  https://github.com/Nikhil-Makwana1/DiscordMediaUploader ⭐️    "

    console_width = shutil.get_terminal_size().columns
    center_offset = (console_width - len(line1)) // 2
    print()
    print(" " * center_offset)
    print(" " * center_offset + line1)
    print(" " * center_offset + line2)
    print(" " * center_offset + line3)
    print(" " * center_offset + line4)
    print(" " * center_offset + line5)
    print()
    print(" " * center_offset + information)
    print()


if __name__ == '__main__':
    logo()
    initialize()
    TOKEN = config.TOKEN

    if not TOKEN:
        TOKEN = input("Discord bot token: ")

    print("Loaded Config: ")
    print("Token: loaded\n")

    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("Invalid token or bot lacks permissions.")
