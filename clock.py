from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=2)
def timed_job():
    print('This should print every 2 minutes')


# @sched.scheduled_job('cron', day_of_week='mon', hour=13)
# def scheduled_job():
#     print('I should print at 1pm')


sched.start()
