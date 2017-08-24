#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from tapioca_github import Github
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from decouple import config


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


OWNER = config('OWNER')
REPO = config('REPO')
GITHUB_KEY = config('GITHUB_KEY')

message = 'http://welcometothedjango.com.br'


github = Github(access_token=GITHUB_KEY, default_url_params=dict(owner=OWNER, repo=REPO))


def submit_news(text):
    issues = github.repo_issues().get()

    for issue in issues:
        number = issue.number().data
        github.issue_comments(number=number).post(data={'body': text})
        break


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    update.message.reply_text(update.message.text)


def newsletter(bot, update):
    #from_user = update.message.reply_to_message.from_user
    #message_id = update.message.reply_to_message.message_id
    text = update.message.reply_to_message.text

    submit_news(text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config('TELEGRAM_BOT_KEY'))

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    #dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("newsletter", newsletter))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
