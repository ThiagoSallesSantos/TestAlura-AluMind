from flask import Blueprint, request, jsonify, abort

from src.model.model import get_model
from src.model.classify_feedback import classify_feedback
from src.model.prompt import get_prompt_classify_feedback

from src.database.models import Feedback, RequestedFeature
from src.database.query import add_db, get_db

from src.routes.utils import *

from src.schemas.schemas import UserFeedbackSchema, RatedFeedbackSchema, RequestedFeatureSchema

route = Blueprint("feedbacks", __name__)

@route.errorhandler(404)
def error_not_found(e):
    return jsonify(error=str(e)), 404

@route.errorhandler(500)
def error_not_found(e):
    return jsonify(error=str(e)), 500

@route.post("/")
def new_classify_feedback() -> RatedFeedbackSchema:
    try:
        feedback = UserFeedbackSchema(**request.json)
        
        model = get_model(**feedback.options.model_dump())
        prompt = get_prompt_classify_feedback()
        rated_feedback = classify_feedback(
            model=model,
            prompt=prompt,
            feedback=feedback
        )

        rated_feedback.id = feedback.id

        session_db = get_session_db()
        feedback_db = Feedback(
            feedback_id=rated_feedback.id,
            feedback_raw=feedback.feedback,
            feedback_sentiment=rated_feedback.sentiment.value,
            feedback_requested_features=[
                RequestedFeature(
                    requested_feature_code=requested_feature.code.value,
                    requested_feature_reason=requested_feature.reason
                )
                for requested_feature in rated_feedback.requested_features
            ]
        )
        add_db(feedback_db, session=session_db)

        return jsonify(rated_feedback.model_dump())
    
    except Exception as e:
        abort(500, description=f"Unexpected error: {e}")

@route.get("/<feedback_id>")
def get_rated_feedback(feedback_id: str) -> RatedFeedbackSchema:
    try:
        session_db = get_session_db()
        feedback: Feedback = get_db(
            table=Feedback,
            session=session_db,
            get_all=False,
            feedback_id=feedback_id
        )

        if feedback is None:
            raise FileNotFoundError("Feedback not found.")

        rated_feedback = RatedFeedbackSchema(
            id=feedback_id,
            sentiment=feedback.feedback_sentiment,
            requested_features=[
                RequestedFeatureSchema(
                    code=requested_feature.requested_feature_code,
                    reason=requested_feature.requested_feature_reason
                )
                for requested_feature in feedback.feedback_requested_features
            ]
        )

        return jsonify(rated_feedback.model_dump())
    
    except FileNotFoundError as e:
        abort(404, description=f"{e}")
    except Exception as e:
        abort(500, description=f"Unexpected error: {e}")
