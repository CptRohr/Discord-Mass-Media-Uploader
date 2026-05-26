# Discord Bot Setup

This guide shows how to create a Discord bot, enable the required intents, and invite it to your server.

## Step 1: Create A Discord Application

1. Open the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application**.
3. Enter a name for the application.
4. Click **Create**.

## Step 2: Create The Bot User

1. Open your application in the Developer Portal.
2. Go to **Bot** in the left sidebar.
3. Click **Add Bot** if a bot user has not already been created.
4. Under **Token**, click **Reset Token** or **Copy Token**.
5. Store the token somewhere private.

Never commit your bot token to GitHub. If a token is exposed, reset it immediately.

## Step 3: Enable Required Intents

In the **Bot** page, scroll to **Privileged Gateway Intents** and enable:

- **Server Members Intent**
- **Message Content Intent**

Message Content Intent is required because this bot listens for commands such as `!kaboom`.

## Step 4: Generate An Invite Link

1. Go to **OAuth2**.
2. Open **URL Generator**.
3. Under **Scopes**, select **bot**.
4. Under **Bot Permissions**, select:
   - **View Channels**
   - **Send Messages**
   - **Attach Files**
   - **Read Message History**
5. Copy the generated URL.

## Step 5: Invite The Bot

1. Open the generated URL in your browser.
2. Select your Discord server.
3. Click **Authorize**.
4. Complete any verification prompts.

After the bot is invited, start `DiscordMediaUploader.py` and run `!kaboom` in the channel where you want files uploaded.
