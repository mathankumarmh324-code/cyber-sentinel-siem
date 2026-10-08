import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from xgboost import XGBClassifier

class DualLayerDetector:
    def __init__(self):
        self.anomaly_model = IsolationForest(contamination=0.1, random_state=42)
        self.classifier_model = XGBClassifier(eval_metric='mlogloss', random_state=42)
        self.is_trained = False

    def predict(self, feature_df):
        feature_cols = ['event_count', 'unique_dest_ports', 'failed_logins', 'total_bytes', 'unique_dests']
        X = feature_df[feature_cols]
        if not self.is_trained:
            anomaly_scores = X['unique_dest_ports'].apply(lambda x: 0.8 if x > 10 else 0.1).values
            class_probs = X['failed_logins'].apply(lambda x: 0.9 if x > 5 else 0.1).values
            predicted_classes = np.where(class_probs > 0.5, 2, 0)
            return anomaly_scores, class_probs, predicted_classes
        raw_anomaly = self.anomaly_model.decision_function(X)
        anomaly_scores = 1 - (raw_anomaly - raw_anomaly.min()) / (raw_anomaly.max() - raw_anomaly.min() + 1e-6)
        probs = self.classifier_model.predict_proba(X)
        return anomaly_scores, np.max(probs, axis=1), np.argmax(probs, axis=1)