from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from Prediction.cron import PrepareProbabilities

scheduler = BackgroundScheduler()
scheduled = False  

def start():
    global scheduled
    if not scheduled:
        scheduler.add_job(PrepareProbabilities, 'cron', hour=5, minute=45) #change the time later making it 00 in nepali time
        scheduler.start()
        scheduled = True