
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta



def schedule_email_task(email_function, email_function_args, delay_seconds):
    # Create and start the scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Calculate the future time for the task
    future_time = datetime.now() + timedelta(seconds=delay_seconds)

    # Create a DateTrigger for the specified run_date
    trigger = DateTrigger(run_date=future_time)

    # Schedule the email sending function with the trigger
    scheduler.add_job(email_function, args=email_function_args, trigger=trigger)
