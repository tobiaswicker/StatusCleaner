# Status Cleaner Bot for Telegram

This bot removes status updates from [Telegram](https://telegram.org) groups and channels.

Status updates include messages like `Foo joined the group [by invite link]`, `Foo added Bar`, `Foo kicked Bar`, 
`Foo changes the group name to «Bar»` and `Foo pinned "<message>"` to name a few.

If you don't want to set up your own bot, feel free to add [@StatusCleanerBot](http://t.me/StatusCleanerBot) to your 
group or channel, promote it to admin and remove all rights except for _Can delete messages_. 

## Installation
1. Clone this repository: `git clone https://github.com/tobiaswicker/StatusCleaner.git`
2. [Download Python 3.x](https://www.python.org/downloads/) if you haven't already
3. Install [Python-Telegram-Bot](https://python-telegram-bot.org) by running `pip install python-telegram-bot` from a 
terminal.
4. Create a bot with [@BotFather](https://t.me/BotFather).
5. Create a username for yourself in the settings of your Telegram account, if you haven't already done so.
6. Rename `config-bot.json.example` to `config-bot.json`, edit it, paste in the `BOT_TOKEN` as well as `YOUR_TELEGRAM_USERNAME`. Remember that this should be _your_ username, **not** your bots username.
7. Run the bot from a terminal: `python statuscleanerbot.py`

## Usage

Add the bot to your group or channel and promote it to admin. The only admin permission required is _Can delete messages_.
