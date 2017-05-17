from django.core.management.base import BaseCommand, CommandError
import os
import time
from project.views import calcvote
from project.models import Story

from apscheduler.schedulers.blocking import BlockingScheduler




class Command(BaseCommand):
    help = "Sets a worker to complete the scheduled calcvote functions"
    requires_model_validation = False
    can_import_settings = True

    def handle(self, **options):
        print("Hello World!")
        sched = BlockingScheduler()
        @sched.scheduled_job('cron', minute='51')
        def scheduled_job():
            print("Updating calcvote jobs.")

            active_stories = Story.objects.filter(finished_story=False)

            for _x in active_stories:
                sched.add_job(calcvote, 'interval', minutes=_x.minutes_between_votes, args=[_x.pk])
        sched.start()
        while True:
            time.sleep(15)


"""
Another possiblity could be to define a function that triggers the beginning of voting, a
and a function that ends it when things.  When a story posts, have the triggering
function called, and when a story finished is True in calcvote, end the job...
Then, wouldn't need to crawl through all the stories each time like this which
is likely ineffecient
In addition, I worry about calling add job on a story that already has an internval
of calcvote going, would they conflict, would it go with the new one and kill the old one?

"""
