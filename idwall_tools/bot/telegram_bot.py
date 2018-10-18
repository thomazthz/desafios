
import os
import logging

from telegram.ext import CommandHandler, Updater
from idwall_tools.crawlers.reddit_scraper import get_high_upvotes_threads


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


HELLO_TEXT = ('Olá, como vai? Espero que bem! Sou o bot do desafio da IDwall. '
              'Ainda estou aprendendo e evoluindo, e no momento sei fazer '
              'apenas duas coisas: posso te ajudar a encontrar as threads que '
              'estão bombando nos seus Subreddits favoritos; '
              'ou posso repetir essa mensagem com /help ou /start.\n'
              'Use o comando "NadaPraFazer" seguido de uma lista '
              'de Subreddits separados por ponto e vírgula.\n '
              'Exemplo: /NadaPraFazer programming;dogs;brasil')


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=HELLO_TEXT)


def help_message(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=HELLO_TEXT)


def error(bot, update, error):
    logger.warning(f'Update "{update}" caused error "{error}"')


def scrape(bot, update, args):
    """Send a list with high upvote threads from one or more Subreddits"""

    if not args or len(args) > 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text=('É quase isso! O comando é assim: \n'
                               '/NadaPraFazer nome_subreddit_1;nome_subreddit_2'))
        return

    subreddits = [subreddit.strip() for subreddit in args[0].split(';')]
    has_at_least_one_thread = {subreddit: None for subreddit in subreddits}
    for i, thread in enumerate(get_high_upvotes_threads(subreddits)):
        has_at_least_one_thread[thread.subreddit] = True

        message = (
            f'#{i+1}\n'
            f'SUBREDDIT: {thread.subreddit}\n'
            f'TÍTULO: {thread.title}\n'
            f'UPVOTES: {thread.upvotes}\n'
            f'URL: {thread.url}\n'
            f'URL (COMENTÁRIOS): {thread.comments_url}\n'

        )
        bot.send_message(chat_id=update.message.chat_id,
                         text=message)

    if not all(has_at_least_one_thread.values()):
        # Filter subreddit names with no threads found
        none_thread = filter(lambda k: not bool(has_at_least_one_thread[k]),
                             has_at_least_one_thread)

        message = ('Não encontrei nenhuma thread bombando '
                   'no(s) seguinte(s) subreddit(s):\n'
                   f'\n{";".join(none_thread)}\n\n'
                   'Verifique se foram digitados corretamente.')

        bot.send_message(chat_id=update.message.chat_id,
                         text=message)


def wake_up():
    token = os.environ.get('TELEGRAM_BOT_TOKEN', None)

    if not token:
        raise ValueError('Telegram bot token not defined. '
                         'Set the env var TELEGRAM_BOT_TOKEN')

    updater = Updater(token=token)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help_message)
    scrape_handler = CommandHandler('NadaPraFazer', scrape, pass_args=True)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(scrape_handler)

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()
