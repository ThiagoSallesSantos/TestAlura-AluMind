from src.database.models import Feedback

from collections import Counter

from src.schemas.schemas import SentimentStatisticsSchema, FeatureStatisticsSchema

from typing import List

def feedback_sentiment_percentage(list_feedbacks: List[Feedback]) -> SentimentStatisticsSchema:
    list_sentiments: List[str] = []
    for feedback in list_feedbacks:
        list_sentiments.append(feedback.feedback_sentiment)
    return SentimentStatisticsSchema(**Counter(list_sentiments))

def most_requested_feature(list_feedbacks: List[Feedback]) -> FeatureStatisticsSchema:
    list_features: List[str] = []
    for feedback in list_feedbacks:
        for requested_feature in feedback.feedback_requested_features:
            list_features.append(requested_feature.requested_feature_code)
    return FeatureStatisticsSchema(**Counter(list_features))