from apscheduler.schedulers.blocking import BlockingScheduler
import requests
sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=2)
def timed_job():
    response = requests.get('http://www.google.com')
    print('This should print every 2 minutes')
    print(response.status_code)


# @sched.scheduled_job('cron', day_of_week='mon', hour=13)
# def scheduled_job():
#     print('I should print at 1pm')


sched.start()
