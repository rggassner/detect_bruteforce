# LDAP Brute-Force Detection (Elasticsearch)

This project detects **successful brute-force attacks** on an LDAP service by analyzing authentication logs stored in Elasticsearch.

It identifies scenarios where:

- A **successful** login occurs
- Within a defined **time window**
- After **N or more failed** attempts
- From the **same user** (`uid`) and **client IP** (`client`)

---

##  How It Works

1. **Log Source**  
   The project expects LDAP bind logs ingested into Elasticsearch, with fields:
   - `uid` → username
   - `client` → IP address of the client
   - `result` → `"success"` or `"fail"`
   - `@timestamp` → event time

2. **Detection Method**  
   For **each successful login** in the last `TIME_WINDOW_MINUTES`:
   - Look backwards `TIME_WINDOW_MINUTES` from that event's timestamp
   - Count failed attempts from the **same uid + client IP**
   - If the fail count ≥ `FAILED_THRESHOLD` → **Alert**

3. **Moving Time Window**  
   This uses a **moving window** (per success event), not fixed buckets.  
   Example with a 5-minute window:  
   - Success at 10:07 → check 10:02–10:07  
   - Success at 10:19 → check 10:14–10:19

---

##  Project Structure

ldap-bruteforce-detector/
├── config.py # All configuration parameters (Elasticsearch + detection)
├── db_connection.py # Elasticsearch connection wrapper
├── detect_bruteforce.py # Main detection script
└── README.md # This file


---

## Configuration

Edit `config.py` to match your environment:


# Elasticsearch connection
ELASTICSEARCH_HOST = '192.168.1.1'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_USER = 'elastic'
ELASTICSEARCH_PASSWORD = 'yourpassword'
ELASTICSEARCH_VERIFY_CERTS = False

# Index pattern
LDAP_INDEX = 'ldap-*'

# Detection parameters
TIME_WINDOW_MINUTES = 5
FAILED_THRESHOLD = 5
FIELD_UID = 'uid'
FIELD_CLIENT_IP = 'client'
FIELD_RESULT = 'result'
FIELD_TIMESTAMP = '@timestamp'

SHOLD = 5
FIELD_UID = 'uid'
FIELD_CLIENT_IP = 'client'
FIELD_RESULT = 'result'
FIELD_TIMESTAMP = '@timestamp'

## Usage

python detect_bruteforce.py
Example output:

[ALERT] Possible brute-force: uid=john.doe, ip=203.0.113.45, fails=7, success_time=2025-08-13T10:07:21Z


## Notes

The script currently queries success events first, then looks back for fails.

It works with a moving time window for better detection accuracy.

For huge datasets, a bucket/aggregation-based approach can be implemented to let Elasticsearch do most of the work.

Works with index patterns like ldap-2025.08, ldap-2025.09, etc., using ldap-*.


## License

This project is licensed under the MIT License. See the LICENSE file for details.
