from pathlib import Path

from log_parser import parse_log_file
from database import create_table, insert_event, get_all_events
from detector import detect_brute_force

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "data" / "sample_auth.log"

def main():
    print("=" * 55)
    print("LOGIN ATTEMPT DETECTION SYSTEM")
    print("=" * 55)

    create_table()
    print("\n[+] Database initialized. ")

    events = parse_log_file(LOG_FILE)
    print(f"[+] Total valid log events: {len(events)}")

    for event in events:
        insert_event(event)
    print(f"[+] Authentication events stored in database.")

    stored_events = get_all_events()
    print(f"[+] Total database records: {len(stored_events)}")

    alerts = detect_brute_force(stored_events)

    print("\n" + "=" * 55)
    print("              Security Alerts")
    print("=" * 55)

    if alerts:
        for alert in alerts:
            print("\n[!] POSSIBLE BRUTE-FORCE ACTIVITY")
            print(f"     IP Address: {alert['ip_address']}")
            print(f"     Failed Attempts: {alert['failed_attempts']}")
            print(f"     Time Window: {alert['window_minutes']} minutes")
            print(f"     First Seen: {alert['first_seen']}")
            print(f"     Last Seen: {alert['last_seen']}")
            print(f"     Details: {alert['message']}")

    else:
        print("\n[+] No suspicious login patterns detected.")

    print("\n" + "=" * 55)
    print("          ANALYSIS COMPLETED")
    print("=" * 55)

if __name__ == "__main__":
    main()