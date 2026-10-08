import json

REQUIRED_FIELDS = ['timestamp', 'source_ip', 'dest_ip', 'event_type']

def process_record(raw_record):
    try:
        data = json.loads(raw_record) if isinstance(raw_record, str) else raw_record
        for field in REQUIRED_FIELDS:
            if field not in data:
                return None
        data['src_port'] = int(data.get('src_port', 0))
        data['dest_port'] = int(data.get('dest_port', 0))
        data['bytes'] = int(data.get('bytes', 0))
        data['auth_status'] = data.get('auth_status', 'N/A')
        return data
    except Exception:
        return None