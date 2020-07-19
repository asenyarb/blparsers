from datetime import datetime, timedelta
from hashlib import md5
import re
import requests
import time

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from backend import parsers_config
from backend.models import Post, PhoneNumber


def process_response_data(data, community_domain):
    keywords = parsers_config.parsers_keywords[community_domain]

    should_continue = True

    time_two_weeks_ago = timezone.now() - timedelta(days=14)

    for post in data['items']:
        text = post['text'].replace("\n", "")

        if post['marked_as_ads']:
            continue

        l_text = text.lower()

        if any(map(lambda word: l_text.find(word) != -1, keywords)):
            phone_numbers = list(
                re.finditer(
                    r'(((\+375|8|80)[-\s]?)?(%s)[-\s]?)?([0-9][-\s]?){7}' % "|".join(parsers_config.operators_codes),
                    text
                )
            )
            phone_numbers = [x.group().strip() for x in phone_numbers]
            date = datetime.utcfromtimestamp(int(post['date'])).astimezone(timezone.get_current_timezone())
            vk_post_id = post['id']
            link = community_domain + "?w=wall{}_{}".format(
                parsers_config.vk_id_by_domain[community_domain], vk_post_id
            )
            text_hash = md5(text.encode()).hexdigest()
            if date < time_two_weeks_ago or Post.objects.filter(
                    Q(external_id=vk_post_id)   # | Q(text_hash=text_hash) MAKE UP ANOTHER WAY!
            ).exists():
                should_continue = False
                break

            if phone_numbers:
                post = Post.objects.create(
                    external_id=vk_post_id,
                    link=link,
                    text=text,
                    text_hash=text_hash,
                    created_date=date
                )
                for number in phone_numbers:
                    PhoneNumber.objects.create(post=post, number=number)

    return should_continue


def get_and_parse_data(community_domain, offset, logger):
    request_url = "{}{}".format(
        settings.VK_API_BASE_URL,
        settings.VK_API_GET_COMMUNITY_WALL_METHOD,
    )

    request_parameters = {
        "access_token": settings.VK_API_TOKEN,
        "v": settings.VK_API_VERSION,
        "domain": community_domain,
        "offset": offset,
        "owner_id": int(parsers_config.vk_id_by_domain[community_domain]),
        "count": 100,
        "marked_as_ads": False
    }

    response_data = requests.get(
        request_url,
        request_parameters
    ).json()['response']

    should_continue = process_response_data(response_data, community_domain)

    should_process_new_request = (len(response_data['items']) == 100) and should_continue

    return should_process_new_request


def parse_vk_community(domain, logger):
    offset = 0

    while get_and_parse_data(domain, offset, logger):
        offset += 100
        time.sleep(1)
