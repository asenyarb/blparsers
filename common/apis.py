from django.conf import settings

import telebot


# Rewrite to task with broadcast rate_limit
class TelegramChannelAPI:
    bot = telebot.TeleBot(settings.TELEGRAM_BOT_API_TOKEN)
    channel_name = settings.TELEGRAM_CHANNEL_NAME
    last_request_sent_datetime = None

    @classmethod
    def send_message(cls, msg):
        return cls.bot.send_message(
            chat_id=cls.channel_name,
            text=msg
        )

    @classmethod
    def edit_message(cls, msg, msg_id):
        return cls.bot.edit_message_text(
            text=msg,
            chat_id=cls.channel_name,
            message_id=msg_id
        )

    @classmethod
    def remove_message(cls, msg_id):
        return cls.bot.delete_message(
            chat_id=cls.channel_name,
            message_id=msg_id
        )
