## Description: This file is the entry point of the application. It is responsible for running the FastAPI application.
from flask import Flask

from src.settings import Settings

from src.routes import *

from apscheduler.schedulers.background import BackgroundScheduler

import atexit

app = Flask(__name__)

@app.get("/version")
def get_version() -> str:
    settings = Settings()
    return settings.version

app.register_blueprint(feedback.route, url_prefix="/feedbacks")
app.register_blueprint(report.route, url_prefix="/report")
app.register_blueprint(email.route, url_prefix="/email")

if __name__ == "__main__":
    settings = Settings()

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=email.send_email, trigger="cron", day_of_week="sat", hour=23, minute=59)
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())

    app.run(
        host=settings.application.app_host,
        port=settings.application.app_port,
        debug=settings.application.app_debug
    )
