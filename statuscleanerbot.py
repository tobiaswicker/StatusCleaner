#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import errno
import json
import logging

from telegram import ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from mwt import MWT  # for caching

logging.basicConfig(format='%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

owner_username = ""


@MWT(timeout=60*60)
def get_admin_ids(chat):
    """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
    return [admin.user.id for admin in chat.get_administrators()]


def start(update: Update, context: CallbackContext):
    """Sends an info message about this bot if /start is called in a private chat or by a group admin."""
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    logger.info(f"Received /start from {user.first_name} [{user.id}] in chat '{chat.title}' [{chat.id}].")

    if user.id in get_admin_ids(chat) or chat.type == 'private':

        text = f"Hello {user.first_name},\n\n" \
               f"this bot removes status notifications from group chats so you will no longer get bugged by messages " \
               f"like `User_x joined the group by invite link`.\n" \
               f"Add this bot to a group, give it admin privileges (granting _Can delete Messages_ is enough) and " \
               f"you are done.\n\n" \
               f"*Enjoy!*\n\n" \
               f"Please report bugs to @{owner_username}."

        message.reply_text(text=text, parse_mode=ParseMode.MARKDOWN)


def delete_message(update: Update, context: CallbackContext):
    """Delete the message provided in update"""
    chat = update.effective_chat
    message = update.effective_message

    logger.info(f"Going to delete message #{message.message_id} from chat '{chat.title}' [{chat.id}].")

    try:
        message.delete()
        logger.info(f"Message #{message.message_id} deleted from chat '{chat.title}' [{chat.id}]")

    except BadRequest:
        message.reply_text(text="Please promote me to admin so I can remove the notification above.")
        logger.error(f"Failed to delete message #{message.message_id} from chat '{chat.title}' [{chat.id}].")


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f'Update "{update}" caused error "{context.error}"')


def main():
    logger.info("Starting Bot.")

    try:
        with open('config-bot.json', 'r', encoding="utf-8") as f:
            config_data = json.load(f)
    except FileNotFoundError:
        logger.error('Could not find config-bot.json. '
                     'Create a copy of config-bot.json.example, modify it and try again.')
        sys.exit(errno.ENOENT)

    bot_token = config_data['BOT_TOKEN']

    global owner_username
    owner_username = config_data['YOUR_TELEGRAM_USERNAME'].replace('@', '')

    # Create the EventHandler and pass it the bot's token.
    updater = Updater(token=bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(MessageHandler(filters=Filters.status_update, callback=delete_message))

    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
