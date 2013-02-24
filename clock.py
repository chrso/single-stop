from apscheduler.scheduler import Scheduler

sched = Scheduler()

@sched.interval_schedule(minutes=3)
def timed_job():
  print 'this job is run every three minutes'

@sched.cron_schedule(day_of_weeks='mon-fri', hour=17)
def scheduled_job():
  print 'this job is run every weekday at 5pm'



sched.start()

while True:
  pass