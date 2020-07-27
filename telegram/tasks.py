from celery.task import Task

from api.models import Publication
from common.apis import TelegramChannelAPI


class TelegramSenderManager(Task):
    rate_limit = "2/m"

    def run(self, publication_id, should_remove=False, **kwargs):
        logger = self.get_logger()

        publication = Publication.objects.get(pk=publication_id)

        if should_remove:
            logger.debug(f"Removing from telegram channel message with id = {publication.external_id}")
            if (
                    publication.status != publication.Status.Published and
                    publication.telegram_message_id is not None
            ):
                return TelegramChannelAPI.remove_message(publication.external_id)
            else:
                logger.warning("Publication is already unpublished or hasn't been published!")
                return

        publication_date = publication.created_date.strftime("%X-%x")
        post_msg = f"{publication.link}\n{publication_date}\n{publication.text}"
        if publication.status == Publication.Status.Draft:
            message = TelegramChannelAPI.send_message(post_msg)
            publication.telegram_message_id = message.message_id
            return
        elif (
                publication.status == Publication.Status.Published and
                publication.telegram_message_id is not None
        ):
            return TelegramChannelAPI.edit_message(post_msg, publication.telegram_message_id)

        logger.warning("Unexpected behavior while sending message to telegram!")
