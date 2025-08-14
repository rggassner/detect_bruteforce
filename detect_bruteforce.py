import datetime
from db_connection import DatabaseConnection
from config import (
    LDAP_INDEX, TIME_WINDOW_MINUTES, FAILED_THRESHOLD,
    FIELD_UID, FIELD_CLIENT_IP, FIELD_RESULT, FIELD_TIMESTAMP
)

def detect_bruteforce():
    db = DatabaseConnection()
    now = datetime.datetime.utcnow()
    start_time = (now - datetime.timedelta(minutes=TIME_WINDOW_MINUTES)).isoformat() + "Z"

    # First, find all successes in the last TIME_WINDOW_MINUTES
    success_query = {
        "bool": {
            "filter": [
                {"term": {FIELD_RESULT: "success"}},
                {"range": {FIELD_TIMESTAMP: {"gte": start_time, "lte": now.isoformat() + "Z"}}}
            ]
        }
    }

    successes = db.search(
        index=LDAP_INDEX,
        query=success_query,
        size=1000
    )["hits"]["hits"]

    for success in successes:
        uid = success["_source"].get(FIELD_UID)
        client_ip = success["_source"].get(FIELD_CLIENT_IP)
        success_time = success["_source"].get(FIELD_TIMESTAMP)

        # Search for failed attempts in the same window before this success
        fail_query = {
            "bool": {
                "filter": [
                    {"term": {FIELD_RESULT: "fail"}},
                    {"term": {FIELD_UID: uid}},
                    {"term": {FIELD_CLIENT_IP: client_ip}},
                    {
                        "range": {
                            FIELD_TIMESTAMP: {
                                "gte": (datetime.datetime.fromisoformat(success_time.replace("Z", "")) -
                                        datetime.timedelta(minutes=TIME_WINDOW_MINUTES)).isoformat() + "Z",
                                "lt": success_time
                            }
                        }
                    }
                ]
            }
        }

        fails = db.search(
            index=LDAP_INDEX,
            query=fail_query,
            size=1000
        )["hits"]["hits"]

        if len(fails) >= FAILED_THRESHOLD:
            print(f"[ALERT] Possible brute-force: uid={uid}, ip={client_ip}, fails={len(fails)}, success_time={success_time}")

    db.close()

if __name__ == "__main__":
    detect_bruteforce()
