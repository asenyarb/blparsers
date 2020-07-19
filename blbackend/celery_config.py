from backend import parsers_config

broker_url = 'amqp://guest:guest@rabbitmq:5672//'
backend = "rpc://"
include = ['backend.tasks']

timezone = 'UTC'
CELERY_ENABLE_UTC = True
# task_ignore_result = True

beat_schedule = {
    'parse-every-10-second-%s' % domain: {
        'task': 'backend.tasks.VKWorkOffersImporter',
        'schedule': 100,
        'args': (domain, )
    } for domain in parsers_config.vk_id_by_domain.keys()
}
