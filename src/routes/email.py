from flask import Blueprint, request, jsonify, abort

from src.database.models import Email
from src.database.query import add_db, get_db, get_after_that

import smtplib

from src.model.email import prepare_report, prepare_email

from datetime import datetime, timedelta

from src.routes.utils import *

from src.settings import Settings

from src.schemas.schemas import EmailSchema

from typing import List

route = Blueprint("email", __name__)

@route.errorhandler(500)
def error_not_found(e):
    return jsonify(error=str(e)), 500

@route.post("/")
def add_email() -> EmailSchema:
    try:
        email = EmailSchema(**request.json)

        session_db = get_session_db()
        email_db = Email(
            email_email = email.email,
            email_name = email.name
        )
        add_db(email_db, session=session_db)

        email.id = email_db.email_id

        return jsonify(email.model_dump())

    except Exception as e:
        abort(500, description=f"Unexpected error: {e}")

## TODO: Transformar em uma rota, caso necessário
def list_emails() -> List[EmailSchema]:
    try:
        session_db = get_session_db()
        list_emails_db: List[Email] = get_db(
            table=Email,
            session=session_db
        )

        list_emails: List[EmailSchema] = [
            EmailSchema(
                id=email_db.email_id,
                email=email_db.email_email,
                name=email_db.email_name
            )
        for email_db in list_emails_db]

        return list_emails

    except Exception as e:
        pass

## TODO: Transformar em uma rota, caso necessário
def send_email():
    try:
        settings = Settings()

        session_db = get_session_db()
        week = datetime.today() - timedelta(days=7)
        list_feedbacks_week = get_after_that(session=session_db, after_that=week)

        report = prepare_report(list_feedbacks=list_feedbacks_week)

        emails = list_emails()
        for email in emails:
            email_message = prepare_email(email=email, report=report)

            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(user=settings.email.email_email, password=settings.email.email_password.get_secret_value())
                smtp.send_message(email_message)
    except Exception as e:
        pass