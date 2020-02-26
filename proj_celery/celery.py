from __future__ import absolute_import
import os
from celery import Celery, shared_task
from django.conf import settings
from core.models import Atualizacao
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj_celery.settings')

app = Celery('proj_celery', backend=settings.BROKER_URL, broker=settings.BROKER_URL)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='America/Sao_Paulo',
    enable_utc=True,
)

# file default: celerybeat-schedule

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(20.0, test.s('PERIODICO'))

    sender.add_periodic_task(
        crontab(minute='*/5'),
        test.s('AGENDADO'),
    )


import datetime

@app.task
def test(arg):
    now = datetime.datetime.now()
    atua = Atualizacao(data=now, tipo=arg)
    atua.save()
    print('TESTEEEEEEEEEEEEEEEEEEEEEEEEE')
    print(arg)



## cmd: celery worker -A proj_celery --pool=solo --loglevel=info
## cmd: celery -A proj_celery beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
## set DJANGO_SETTINGS_MODULE=proj_celery.settings
## cmd: celery -A proj_celery beat --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler