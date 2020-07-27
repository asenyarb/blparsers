from __future__ import absolute_import, unicode_literals
from celery.task import Task
from celery.five import monotonic
from contextlib import contextmanager
from django.core.cache import cache
from hashlib import md5
from parsers.vkparser.parser import VKParser


LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes


@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = monotonic() + LOCK_EXPIRE - 3
    # cache.add fails if the key already exists
    status = cache.add(lock_id, oid, LOCK_EXPIRE)
    try:
        yield status
    finally:
        # memcache delete is very slow, but we have to use it to take
        # advantage of using add() for atomic locking
        if monotonic() < timeout_at and status:
            # don't release the lock if we exceeded the timeout
            # to lessen the chance of releasing an expired lock
            # owned by someone else
            # also don't release the lock if we didn't acquire it
            cache.delete(lock_id)


class VKWorkOffersImporter(Task):
    name = "parse.vk"

    def run(self, domain, **kwargs):
        logger = self.get_logger(**kwargs)

        feed_url_hexdigest = md5(domain.encode()).hexdigest()
        lock_id = '{0}-lock-{1}'.format(self.name, feed_url_hexdigest)
        logger.warning('Importing feed: %s', domain)
        with memcache_lock(lock_id, self.app.oid) as acquired:
            if acquired:
                VKParser.parse_vk_community(domain, logger)
                logger.warning("Parsed community %s" % domain)
                return
        logger.warning('Feed %s is already being imported by another worker', domain)
