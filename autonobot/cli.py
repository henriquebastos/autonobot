from tapioca_github import Github
from telegram.ext import Updater, CommandHandler
import logging
from decouple import config


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


OWNER = config('OWNER')
REPO = config('REPO')
GITHUB_KEY = config('GITHUB_KEY')
INSTRUCTIONS = """Pra quem tá chegando e quer entender o que é /newsletter:

Eu e a Evelin enviamos uma newsletter semanal chamada Curto Circuito com as melhores dicas da galera.

Você pode se inscrever em http://hbn.link/cc-assine

Você pode contribuir manualmente para a próxima edição em http://hbn.link/cc-contribua

Além disso, quando você ver uma mensagem, nesse grupo, com um link massa que merece ir para o CC, você pode:

1) Marcar a mensagem
2) Fazer reply da mensagem apenas com o texto: /newsletter

Assim o @autonobot vai automagicamente registrar sua sugestão para a próxima edição.

PS: É importante que o comando /newsletter aconteça como REPLY da mensagem contendo o link.
"""


github = Github(access_token=GITHUB_KEY, default_url_params=dict(owner=OWNER, repo=REPO))


def submit_news(text):
    issues = github.repo_issues().get()

    for issue in issues:
        number = issue.number().data
        github.issue_comments(number=number).post(data={'body': text})
        break


def newsletter(bot, update):
    #from_user = update.message.reply_to_message.from_user
    #message_id = update.message.reply_to_message.message_id

    if update.message.reply_to_message:  # post link to GitHub issue
        text = update.message.reply_to_message.text
        submit_news(text)

    else:  # post instructions on Telegram
        update.message.reply_text(INSTRUCTIONS)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config('TELEGRAM_BOT_KEY'))

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("newsletter", newsletter))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
