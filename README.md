# Duck Central Cogs — `go_live`

A custom Red DiscordBot cog for manually posting a Twitch go-live announcement.

## Features

- `[p]go-live` posts an embed and pings a configured Discord role.
- `[p]go-live your message here` uses a one-time custom message.
- Configure the role, announcement channel, Twitch URL, embed title, and default message.
- Settings are stored per server and persist through bot restarts.
- Role mentions are explicitly allowed for the configured role only; `@everyone` and user mentions are not enabled by the cog.

## Requirements

- Red DiscordBot 3.5.x
- Python version supported by your Red installation

## Install from your own GitHub repository

1. Upload this repository to GitHub. Keep `info.json` at the repository root and the `go_live/` folder in place.
2. In Discord, add the repository to Red (replace the URL with your repository's raw GitHub URL):

   ```text
   [p]repo add duckcentralcogs https://github.com/YOUR-USERNAME/YOUR-REPO
   ```

3. Install and load the cog:

   ```text
   [p]cog install duckcentralcogs go_live
   [p]load go_live
   ```

   If your Red version's repository setup expects a different URL format, follow its repo-add prompt/documentation.

## First-time setup

Run these commands as a server administrator. Replace the placeholders with the role and channel from your server:

```text
[p]golive setrole @Twitch Notifications
[p]golive setchannel #stream-announcements
[p]golive seturl https://twitch.tv/wantedduck125
[p]golive settitle 🔴 WantedDuck125 is LIVE on Twitch!
[p]golive setmessage I'm live on Twitch! Come hang out.
[p]golive
```

Then, whenever you go live, run:

```text
[p]go-live
```

Or add a custom message for that stream:

```text
[p]go-live SCP: Secret Laboratory — trying to escape again!
```

`[p]` is Red's configured command prefix; use your actual prefix in place of it.

## Permissions

The bot needs permission to view the configured channel, send messages, embed links, and mention the selected role. Depending on the server's role hierarchy and mentionable-role settings, Discord server permissions may also need adjustment. The cog's AllowedMentions configuration allows only the configured role mention in the announcement.

## Commands

| Command | Purpose |
|---|---|
| `[p]go-live [message]` | Post the announcement and ping the configured role |
| `[p]golive` | Show current settings |
| `[p]golive setrole @role` | Choose the role to ping |
| `[p]golive setchannel #channel` | Choose the announcement channel |
| `[p]golive seturl <url>` | Set Twitch channel URL |
| `[p]golive settitle <title>` | Change the embed title |
| `[p]golive setmessage <message>` | Change the default announcement text |
| `[p]golive reset` | Reset this server's settings |

## Notes

- This cog does not detect Twitch streams automatically. You run `[p]go-live` manually.
- The default Twitch URL is `https://twitch.tv/wantedduck125`; change it with `seturl` if needed.
- This is a starter cog. Test it in a private channel before using it for live announcements.
