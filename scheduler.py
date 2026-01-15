from apscheduler.schedulers.background import BackgroundScheduler
from update_data import run_pipeline_multithread

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(run_pipeline_multithread, 'interval', minutes=10, id="crypto_scraping")
    scheduler.start()
    print("Scheduler lancé : scraping toutes les 10 min")

def shutdown_scheduler():
    scheduler.shutdown(wait=False)
    print("Scheduler arrêté")