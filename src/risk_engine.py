def calculate_risk_and_evidence(row, anomaly_score, class_prob):
    risk_score = 0
    evidence = []
    if row['failed_logins'] >= 3:
        risk_score += 40
        evidence.append(f"High failed login attempts: {row['failed_logins']} failures")
    if row['unique_dest_ports'] >= 15:
        risk_score += 30
        evidence.append(f"Port scanning pattern detected: {row['unique_dest_ports']} unique ports")
    if row['total_bytes'] > 50_000_000:
        risk_score += 30
        evidence.append(f"High outbound traffic: {row['total_bytes'] / (1024*1024):.2f} MB")
    risk_score += int(anomaly_score * 20) + int(class_prob * 30)
    risk_score = min(100, max(0, risk_score))
    classification = "Normal" if risk_score <= 30 else ("Suspicious" if risk_score <= 70 else "Malicious")
    return risk_score, classification, " | ".join(evidence) if evidence else "Routine behavior"