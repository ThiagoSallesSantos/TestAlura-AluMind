from flask import Blueprint, render_template, jsonify, abort

from src.database.models import Feedback, RequestedFeature
from src.database.query import get_db

from src.model.statistics import feedback_sentiment_percentage, most_requested_feature

from src.routes.utils import *

from src.schemas.schemas import Sentiment, CodeFeature

from typing import List

route = Blueprint("report", __name__)

@route.errorhandler(500)
def error_not_found(e):
    return jsonify(error=str(e)), 500

@route.get("/")
def get_report():
    try:
        session_db = get_session_db()
        list_feedbacks: List[Feedback] = get_db(
            table=Feedback,
            session=session_db
        )

        sentiment_percentage = feedback_sentiment_percentage(list_feedbacks=list_feedbacks)
        requested_features = most_requested_feature(list_feedbacks=list_feedbacks)

        return render_template("report.html", sentiment_percentage=sentiment_percentage, requested_features=requested_features, list_feedbacks=list_feedbacks)
    except Exception as e:
        abort(500, description=f"Unexpected error: {e}")

@route.get("/<data>")
def get_feedbacks_by_data(data: str):
    try:
        list_feedbacks: List[Feedback] = []

        if data in Sentiment.values():
            session_db = get_session_db()
            list_feedbacks = get_db(
                table=Feedback,
                session=session_db,
                feedback_sentiment=data
            )

        if data in CodeFeature.values():
            session_db = get_session_db()
            list_requested_features: List[RequestedFeature] = get_db(
                table=RequestedFeature,
                session=session_db,
                requested_feature_code=data
            )

            list_feedbacks = [requested_feature.feedback for requested_feature in list_requested_features]

        return render_template("report.html", list_feedbacks=list_feedbacks)
    except Exception as e:
        abort(500, description=f"Unexpected error: {e}")

