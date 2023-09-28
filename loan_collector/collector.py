from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from loan_collector import collect_loan

def start():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(collect_loan.check_expired_loans, 'interval', minutes=1500)