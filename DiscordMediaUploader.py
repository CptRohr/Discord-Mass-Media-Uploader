import datetime
import os
import shutil
import discord
from discord.ext import commands
import config

LARGE_MEDIA = ""
CONTENT_FOLDER = ""
LOG_FILE = ""
MAX_FILES_PER_MESSAGE = 10

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


def should_skip_file(filename):
    return filename.startswith(".")


def file_info(file_path):
    filesize = os.path.getsize(file_path) / (1024 * 1024)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return filesize, current_time


def log_uploaded_file(log_file, filename, filesize, current_time):
    log_file.write(f"{current_time} {filesize:10.2f}    {filename}\n")
    print(f"Uploaded: {current_time} {filesize:6.2f} MB  {filename}")


def move_to_large(file_path, filename):
    large_file_path = os.path.join(LARGE_MEDIA, filename)
    shutil.move(file_path, large_file_path)
    print(f"Too large: {filename}")


def chunk_files(files, chunk_size):
    for index in range(0, len(files), chunk_size):
        yield files[index:index + chunk_size]


async def send_single_file(channel, log_file, upload):
    filename = upload["filename"]
    file_path = upload["path"]
    discord_file = None

    try:
        filesize, current_time = file_info(file_path)
        discord_file = discord.File(file_path, filename)
        await channel.send(file=discord_file)
        log_uploaded_file(log_file, filename, filesize, current_time)
        return True
    except Exception as e:
        if "Payload Too Large" in str(e):
            move_to_large(file_path, filename)
        else:
            print(f"Failed to upload {filename}: {e}")

        return False
    finally:
        if discord_file:
            discord_file.close()


async def send_file_batch(channel, log_file, uploads):
    discord_files = []

    try:
        for upload in uploads:
            discord_files.append(discord.File(upload["path"], upload["filename"]))

        await channel.send(files=discord_files)

        for upload in uploads:
            filesize, current_time = file_info(upload["path"])
            log_uploaded_file(log_file, upload["filename"], filesize, current_time)

        return len(uploads), 0
    except Exception as e:
        print(f"Batch upload failed, retrying one by one: {e}")

        uploaded_count = 0
        failed_count = 0

        for upload in uploads:
            if await send_single_file(channel, log_file, upload):
                uploaded_count += 1
            else:
                failed_count += 1

        return uploaded_count, failed_count
    finally:
        for discord_file in discord_files:
            discord_file.close()


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
    uploads = []

    for filename in os.listdir(CONTENT_FOLDER):
        file_path = os.path.join(CONTENT_FOLDER, filename)

        if not os.path.isfile(file_path):
            continue

        if should_skip_file(filename):
            continue

        if not upload_all and filename in logs:
            skipped_count += 1
            continue

        uploads.append({
            "filename": filename,
            "path": file_path
        })

    with open(LOG_FILE, 'a') as file:
        for upload_batch in chunk_files(uploads, MAX_FILES_PER_MESSAGE):
            batch_uploaded_count, batch_failed_count = await send_file_batch(channel, file, upload_batch)
            uploaded_count += batch_uploaded_count
            failed_count += batch_failed_count

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
    credit = "    Modified by CptRohr  |  https://github.com/CptRohr    "

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
    print(" " * center_offset + credit)
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
