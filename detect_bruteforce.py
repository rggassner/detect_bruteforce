#!venv/bin/python3
import datetime
from db_connection import DatabaseConnection
from config import *

def log_debug(message):
    """Helper to log only if DEBUG is enabled."""
    if DEBUG:
        print(f"[DEBUG] {message}")


def get_unique_pairs(db, month_start, now):
    """
    Scroll through all events in the last LOOKBACK_DAYS and collect unique (uid, ip) pairs.
    """
    pairs = set()
    total_events = 0

    base_query = {
        "bool": {
            "filter": [
                {"term": {FIELD_LDAP_VERB: "BIND"}},
                {"range": {FIELD_TIMESTAMP: {"gte": month_start, "lte": now.isoformat() + "Z"}}}
            ]
        }
    }

    log_debug("Starting scroll to collect unique uid/ip pairs...")
    res = db.search(
        index=LDAP_INDEX,
        query=base_query,
        size=SCROLL_PAGE_SIZE,
        scroll=SCROLL_TIMEOUT
    )

    scroll_id = res.get("_scroll_id")
    hits = res["hits"]["hits"]

    while hits:
        total_events += len(hits)
        log_debug(f"Scrolled {total_events} events so far... found {len(pairs)} unique pairs.")

        for hit in hits:
            src = hit["_source"]
            uid = src.get(FIELD_UID)
            ip = src.get(FIELD_CLIENT_IP)
            if uid and ip:
                pairs.add((uid, ip))

        res = db.scroll(scroll_id=scroll_id, scroll=SCROLL_TIMEOUT)
        scroll_id = res.get("_scroll_id")
        hits = res["hits"]["hits"]

    db.clear_scroll(scroll_id=scroll_id)
    log_debug(f"Finished scrolling. Total events scanned: {total_events}")
    return pairs


def detect_bruteforce():
    db = DatabaseConnection()
    now = datetime.datetime.now(datetime.UTC)
    month_start = (now - datetime.timedelta(days=LOOKBACK_DAYS)).isoformat() + "Z"

    # Step 1: Get all unique uid/ip pairs via scroll
    pairs = get_unique_pairs(db, month_start, now)
    print(f"[INFO] Found {len(pairs)} unique uid/ip pairs in the last {LOOKBACK_DAYS} days.")

    # Step 2: Check brute-force for each pair
    for idx, (uid, client_ip) in enumerate(pairs, start=1):
        log_debug(f"Processing pair {idx}/{len(pairs)}: uid={uid}, ip={client_ip}")

        success_query = {
            "bool": {
                "filter": [
                    {"term": {FIELD_RESULT: "LDAP_SUCCESS"}},
                    {"term": {"requests.verb.keyword": "BIND"}},
                    {"term": {FIELD_UID: uid}},
                    {"term": {FIELD_CLIENT_IP: client_ip}},
                    {"range": {FIELD_TIMESTAMP: {"gte": month_start, "lte": now.isoformat() + "Z"}}}
                ]
            }
        }

        successes = db.search(index=LDAP_INDEX, query=success_query, size=1000)["hits"]["hits"]
        log_debug(f"Found {len(successes)} successes for uid={uid}, ip={client_ip}")

        for success in successes:
            success_time = success["_source"].get(FIELD_TIMESTAMP)
            success_dt = datetime.datetime.fromisoformat(success_time.replace("Z", ""))

            fail_query = {
                "bool": {
                    "filter": [
                        {"term": {FIELD_RESULT: "LDAP_INVALID_CREDENTIALS"}},
                        {"term": {FIELD_UID: uid}},
                        {"term": {FIELD_CLIENT_IP: client_ip}},
                        {
                            "range": {
                                FIELD_TIMESTAMP: {
                                    "gte": (success_dt - datetime.timedelta(minutes=TIME_WINDOW_MINUTES)).isoformat() + "Z",
                                    "lt": success_time
                                }
                            }
                        }
                    ]
                }
            }

            fails = db.search(index=LDAP_INDEX, query=fail_query, size=1000)["hits"]["hits"]

            if len(fails) >= FAILED_THRESHOLD:
                print(f"[ALERT] Possible brute-force: uid={uid}, ip={client_ip}, fails={len(fails)}, success_time={success_time}")

    db.close()


if __name__ == "__main__":
    detect_bruteforce()
