import pandas as pd

def extract_window_features(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    features = []
    for source_ip, group in df.groupby('source_ip'):
        group = group.sort_values('timestamp')
        features.append({
            'source_ip': source_ip,
            'event_count': len(group),
            'unique_dest_ports': group['dest_port'].nunique(),
            'failed_logins': len(group[group['auth_status'] == 'FAILED']),
            'total_bytes': group['bytes'].sum(),
            'unique_dests': group['dest_ip'].nunique()
        })
    return pd.DataFrame(features)