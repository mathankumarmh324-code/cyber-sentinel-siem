import sys
import time
import argparse
import pandas as pd
from src.ingestion import process_record
from src.features import extract_window_features
from src.detection import DualLayerDetector
from src.risk_engine import calculate_risk_and_evidence
from src.database import init_db, log_alert

def process_and_log(file_path, detector):
    init_db()
    try:
        raw_df = pd.read_json(file_path)
    except Exception:
        return

    if raw_df.empty:
        return

    valid_records = [process_record(r) for r in raw_df.to_dict(orient='records')]
    valid_records = [r for r in valid_records if r is not None]
    
    if not valid_records:
        return

    clean_df = pd.DataFrame(valid_records)
    feature_df = extract_window_features(clean_df)
    anomaly_scores, class_probs, _ = detector.predict(feature_df)

    for idx, row in feature_df.iterrows():
        risk, label, evidence = calculate_risk_and_evidence(row, anomaly_scores[idx], class_probs[idx])
        log_alert(row['source_ip'], label, risk, evidence)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True)
    parser.add_argument("--max-risk", type=int, default=70)
    parser.add_argument("--interval", type=int, default=3)
    args = parser.parse_args()

    detector = DualLayerDetector()
    print("🛡️ Cyber Sentinel Live Monitoring Started... (Press Ctrl+C to stop)")

    while True:
        try:
            process_and_log(args.file, detector)
            time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
            break

if __name__ == "__main__":
    main()