from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from Auth.notification import send_notification_to_token

scheduler = BackgroundScheduler()
scheduled = False  

def start():
    global scheduled
    if not scheduled:
        scheduler.add_job(send_notification_to_token, 'cron', hour=2, minute=45) 
        scheduler.start()
        scheduled = True