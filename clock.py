from apscheduler.schedulers.blocking import BlockingScheduler
from main import bot
import getprices

beer_list = ['branik', 'svijany', 'gambrinus']


sched = BlockingScheduler()

@sched.scheduled_job('cron', day='*', hour=7)
def scheduled_job():
    for beer in beer_list:
        getprices.parse_beer(beer)
    bot.send_message(203013998, 'Updated prices')
    print('This job is run every day at 7.')

sched.start()
