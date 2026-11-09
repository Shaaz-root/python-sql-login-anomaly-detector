from datetime import datetime, timedelta


def detect_brute_force(events, threshold=5, window_minutes=5):

    alerts = []

    failed_events = []

    for event in events:
        if event["status"].upper() == "FAILED":

            event = event.copy()

            if isinstance(event["timestamp"], str):
                event["timestamp"] = datetime.strptime(
                    event["timestamp"],
                    "%Y-%m-%d %H:%M:%S"
                )

            failed_events.append(event)

    failed_events.sort(key=lambda event: event["timestamp"])

    window = timedelta(minutes=window_minutes)

    for current_event in failed_events:

        start_time = current_event["timestamp"] - window
        end_time = current_event["timestamp"]

        matching_events = [
            event for event in failed_events
            if event["ip_address"] == current_event["ip_address"]
            and start_time < event["timestamp"] <= end_time
        ]

        if len(matching_events) >= threshold:

            alert = {
                "ip_address": current_event["ip_address"],
                "failed_attempts": len(matching_events),
                "window_minutes": window_minutes,
                "first_seen": matching_events[0]["timestamp"],
                "last_seen": current_event["timestamp"],
                "message": (
                    f"Possible brute-force activity from "
                    f"{current_event['ip_address']}: "
                    f"{len(matching_events)} failed login attempts "
                    f"within {window_minutes} minutes."
                ),
            }

            if not any(
                existing["ip_address"] == alert["ip_address"]
                and existing["last_seen"] == alert["last_seen"]
                for existing in alerts
            ):
                alerts.append(alert)

    return alerts