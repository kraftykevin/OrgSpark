from django.core.management.base import BaseCommand, CommandError
import os
import time
from project.views import calcvote1, calcvote2, calcvote3, calcvote4

from apscheduler.schedulers.blocking import BlockingScheduler



class Command(BaseCommand):
    help = "Sets a worker to complete the scheduled calcvote functions"
    requires_model_validation = False
    can_import_settings = True

    def handle(self, **options):
        print("Hello World!")
        sched = BlockingScheduler()
        sched.add_job(calcvote1, 'cron', minute='00')
        sched.add_job(calcvote2, 'cron', minute='15')
        sched.add_job(calcvote3, 'cron', minute='30')
        sched.add_job(calcvote4, 'cron', minute='45')
        sched.start()

        while True:
            time.sleep(10)
