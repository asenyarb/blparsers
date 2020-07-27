from parsers.vkparser import parser_config

broker_url = 'amqp://guest:guest@rabbitmq:5672//'
backend = "rpc://"
include = ['parsers.tasks', 'telegram.tasks']

timezone = 'UTC'
CELERY_ENABLE_UTC = True
# task_ignore_result = True

beat_schedule = {
    'parse-every-10-second-%s' % domain: {
        'task': 'parse.vk',
        'schedule': 600,
        'args': (domain, ),
    } for domain in parser_config.vk_id_by_domain.keys()
}

task_routes = {
    'telegram.tasks.TelegramSenderManager': {'queue': 'telegram_channel'},
}
