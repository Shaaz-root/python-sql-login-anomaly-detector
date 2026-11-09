from datetime import datetime


def parse_log_line(line):
    

    try:
        parts = line.strip().split(" | ")

        timestamp = datetime.strptime(
            parts[0], "%Y-%m-%d %H:%M:%S"
        )

        username = parts[1].split("=", 1)[1]
        ip_address = parts[2].split("=", 1)[1]
        status = parts[3].split("=", 1)[1]

        if status not in ("SUCCESS", "FAILED"):
            return None

        return {
            "timestamp": timestamp,
            "username": username,
            "ip_address": ip_address,
            "status": status,
        }

    except (ValueError, IndexError):
        return None


def parse_log_file(file_path):
    

    events = []

    with open(file_path, "r", encoding="utf-8") as log_file:
        for line in log_file:
            event = parse_log_line(line)

            if event is not None:
                events.append(event)

    return events