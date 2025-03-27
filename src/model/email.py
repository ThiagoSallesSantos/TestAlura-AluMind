from email.message import EmailMessage

from src.settings import Settings

from src.database.models import Feedback, RequestedFeature

from src.model.statistics import feedback_sentiment_percentage

from src.model.model import get_model
from src.model.prompt import get_prompt_report

from src.schemas.schemas import EmailSchema, ReportSchema

from tabulate import tabulate

from typing import List

def prepare_report(list_feedbacks: List[Feedback]) -> str:
    settings = Settings()
    sentiment_percentage = feedback_sentiment_percentage(list_feedbacks=list_feedbacks)

    table = [
        [sentiment, getattr(sentiment_percentage, sentiment), f"{round(getattr(sentiment_percentage, sentiment)/sentiment_percentage.total * 100, 2)}%"]
        for sentiment in sentiment_percentage.fields
    ]

    list_features: List[RequestedFeature] = []
    for feedback in list_feedbacks:
        list_features.extend(feedback.feedback_requested_features)

    model = get_model(model=settings.email.email_model, apo_key=settings.email.email_api_key)
    prompt = get_prompt_report()
    model_structed = model.with_structured_output(ReportSchema)

    chain = prompt | model_structed
    report: ReportSchema = chain.invoke({"features": list_features})

    main_features = "\n".join(f"- {features}" for features in report.main_features)
    main_reasons = "\n".join(f"- {reasons}" for reasons in report.main_reasons)
    return f"""
{tabulate(table, headers=["Sentiment", "total", "%"])}
Main features:
{main_features}
Main Reasons:
{main_reasons}
"""

def prepare_email(email: EmailSchema, report: str) -> EmailMessage:
    settings = Settings()

    email_message = EmailMessage()
    email_message["Subject"] = "Relatório Semanal - AluMind"
    email_message["From"] = settings.email.email_email
    email_message["To"] = email.email

    email_message.set_content(f"""
Sr(a) {email.name}.
Segue o relatório semanal da AluMind:
{report}
att: Equipe da AluMind
""")

    return email_message
