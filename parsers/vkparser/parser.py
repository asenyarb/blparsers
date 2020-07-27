from datetime import datetime, timedelta
from hashlib import md5
import re
import requests
import time

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from parsers.vkparser import parser_config
from parsers.vkparser.models import VKPost
from api.models import PublicationPhoneNumber
from telegram.tasks import TelegramSenderManager


class VKParser:
    @classmethod
    def get_phone_numbers_from_text(cls, text):
        regex_pattern = r'(([\+]?(%s)[-\s]?)?(%s)[-\s]?)?([0-9][-\s]?){7}' % (
            "|".join(parser_config.country_codes),
            "|".join(parser_config.operators_codes)
        )
        found_regex_matches = re.finditer(
            regex_pattern,
            text
        )

        return [
            x.group().strip() for x in found_regex_matches
        ]

    @classmethod
    def process_response_data(cls, data, community_domain, logger):
        keywords = parser_config.parsers_keywords[community_domain]

        should_continue = True

        time_two_weeks_ago = timezone.now() - timedelta(days=14)

        posts_to_publish = []

        for post in data['items']:
            text = post['text'].replace("\n", "")

            if post['marked_as_ads']:
                continue

            l_text = text.lower()

            if any(map(lambda word: l_text.find(word) != -1, keywords)):
                phone_numbers = cls.get_phone_numbers_from_text(text)

                date = datetime.utcfromtimestamp(int(post['date'])).astimezone(timezone.get_current_timezone())

                vk_post_id = post['id']
                link = community_domain + "?w=wall{}_{}".format(
                    parser_config.vk_id_by_domain[community_domain], vk_post_id
                )
                text_hash = md5(text.encode()).hexdigest()

                if date < time_two_weeks_ago:
                    should_continue = False
                    break

                if phone_numbers:
                    post, created = VKPost.objects.get_or_create(
                        external_id=vk_post_id,
                        defaults={
                            'link': link,
                            'text': text,
                            'text_hash': text_hash,
                            'created_date': date
                        }
                    )

                    for number in phone_numbers:
                        PublicationPhoneNumber.objects.get_or_create(
                            publication=post.publication_ptr, number=number
                        )

                    edited = False
                    if not created and text_hash != post.text_hash:
                        post.text_hash = text_hash
                        post.text = text
                        post.save()
                        edited = True

                    if created or edited:
                        posts_to_publish.append(post.publication_ptr)
                else:
                    logger.debug(f"No phone numbers found in {text}.\nSkipping.")

        return should_continue, posts_to_publish

    @classmethod
    def get_and_parse_data(cls, community_domain, offset, logger):
        request_url = "{}{}".format(
            settings.VK_API_BASE_URL,
            settings.VK_API_GET_COMMUNITY_WALL_METHOD,
        )

        request_parameters = {
            "access_token": settings.VK_API_TOKEN,
            "v": settings.VK_API_VERSION,
            "domain": community_domain,
            "offset": offset,
            "owner_id": int(parser_config.vk_id_by_domain[community_domain]),
            "count": 100,
            "marked_as_ads": False
        }

        r = requests.get(
            request_url,
            request_parameters
        ).json()
        response_data = r['response']

        should_continue, posts_to_publish = cls.process_response_data(response_data, community_domain, logger)

        should_process_new_request = (len(response_data['items']) == 100) and should_continue

        return should_process_new_request, posts_to_publish

    @classmethod
    def parse_vk_community(cls, domain, logger):
        offset = 0
        should_continue = True

        posts_to_publish = []

        while should_continue:
            should_continue, additional_posts_to_publish = cls.get_and_parse_data(domain, offset, logger)
            posts_to_publish.extend(additional_posts_to_publish)
            offset += 100
            time.sleep(1)

        for post in sorted(posts_to_publish, key=lambda p: p.created_date):
            TelegramSenderManager.delay(post.pk)
