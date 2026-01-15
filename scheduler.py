from apscheduler.schedulers.background import BackgroundScheduler
from update_data import run_pipeline

scheduler = BackgroundScheduler()

def start_scheduler():
    """
    Démarre le scheduler APScheduler pour exécuter le pipeline automatiquement.
    """
    scheduler.add_job(run_pipeline, 'interval', minutes=10, id="crypto_scraping")

    scheduler.start()
    print("Scheduler lancé : scraping automatique toutes les 10 minutes")


def shutdown_scheduler():
    """
    Arrête proprement le scheduler APScheduler.
    """
    scheduler.shutdown(wait=False)
    print("Scheduler arrêté proprement")