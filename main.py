import win32evtlog
import json
import requests
import os
from datetime import datetime, timedelta
import time
from collections import deque

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Discord Webhook URL from .env file
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Event IDs for various events
EVENT_IDS = {
    4720: "👤 User Account Created", # User account created
    4726: "🗑️ User Account Deleted", # User account deleted
    4738: "✏️ User Account Modified", # User account modified
    1102: "⚠️ Audit Log Cleared",  # Audit log cleared
    4778: "🔄 RDP Session Reconnected",  # RDP session reconnected
    4779: "🔌 RDP Session Disconnected",  # RDP session disconnected
}

# Queue to hold events before sending
event_queue = deque()
# Dictionary to track recently logged events to avoid duplicates
recent_events = {}
# Time window for duplicate detection
DUPLICATE_TIME_WINDOW = timedelta(seconds=30)

# Function to send data to Discord immediately
def send_to_discord(event_data):
    embed = {
        "title": event_data["event_type"],
        "color": 3066993 if "Successful" in event_data["event_type"] else 15158332,
        "fields": [
            {"name": "🆔 Event ID", "value": event_data["event_id"], "inline": True},
            {"name": "👤 Username", "value": event_data.get("username", "Unknown"), "inline": True},
            {"name": "🌐 Source IP", "value": event_data.get("source_ip", "Unknown"), "inline": True},
            {"name": "⏰ Time", "value": event_data["time"], "inline": False},
            {"name": "📍 Logon Info", "value": event_data.get("logon_info", "Unknown"), "inline": False},
        ],
    }
    embed["fields"] = [field for field in embed["fields"] if field is not None]  # Remove None fields
    data = {"embeds": [embed]}
    response = requests.post(WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print("Event sent to Discord successfully.")
    else:
        print(f"Failed to send event to Discord: {response.status_code}, {response.text}")

# Function to send batch data to Discord
def send_to_discord_batch():
    if not event_queue:
        return

    embeds = []
    while event_queue and len(embeds) < 10:  # Batch up to 10 events per message
        event_data = event_queue.popleft()
        embed = {
            "title": event_data["event_type"],
            "color": 3066993 if "Successful" in event_data["event_type"] else 15158332,
            "fields": [
                {"name": "🆔 Event ID", "value": event_data["event_id"], "inline": True},
                {"name": "👤 Username", "value": event_data.get("username", "Unknown"), "inline": True},
                {"name": "🌐 Source IP", "value": event_data.get("source_ip", "Unknown"), "inline": True},
                {"name": "⏰ Time", "value": event_data["time"], "inline": False},
                {"name": "📍 Logon Info", "value": event_data.get("logon_info", "Unknown"), "inline": False},
            ],
        }
        embed["fields"] = [field for field in embed["fields"] if field is not None]  # Remove None fields
        embeds.append(embed)

    data = {"embeds": embeds}
    response = requests.post(WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print("Batch sent to Discord successfully.")
    else:
        print(f"Failed to send batch to Discord: {response.status_code}, {response.text}")

# Function to monitor Windows Event Logs
def monitor_event_logs():
    server = "localhost"
    log_type = "Security"
    hand = win32evtlog.OpenEventLog(server, log_type)

    while True:
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        events = win32evtlog.ReadEventLog(hand, flags, 0)

        if events:
            for event in events:
                if event.EventID in EVENT_IDS:
                    event_data = {
                        "event_id": event.EventID,
                        "event_type": EVENT_IDS[event.EventID],
                        "time": event.TimeGenerated.strftime("%Y-%m-%d %H:%M:%S"),
                    }

                    # Extract additional information from the event description
                    description = event.StringInserts
                    if description:
                        try:
                            if event.EventID in [4720, 4726, 4738]:
                                event_data["username"] = description[0]  # Account Name
                            elif event.EventID in [4778, 4779]:
                                event_data["username"] = description[1]  # User for RDP session
                                event_data["source_ip"] = description[2]  # Source IP for RDP session
                                send_to_discord(event_data)  # Send RDP session events immediately
                                continue
                        except IndexError:
                            pass

                    # Check for duplicates
                    event_key = (event_data.get("username"), event_data.get("source_ip"), event_data["event_id"])
                    current_time = datetime.strptime(event_data["time"], "%Y-%m-%d %H:%M:%S")

                    if event_key in recent_events:
                        last_logged_time = recent_events[event_key]
                        if current_time - last_logged_time < DUPLICATE_TIME_WINDOW:
                            continue  # Skip duplicate

                    # Update recent events and add to queue
                    recent_events[event_key] = current_time
                    event_queue.append(event_data)

        # Send batch to Discord with a delay
        send_to_discord_batch()
        time.sleep(5)  # Delay to avoid hitting rate limits

if __name__ == "__main__":
    if WEBHOOK_URL is None:
        print("Error: DISCORD_WEBHOOK_URL is not set in the .env file.")
    else:
        monitor_event_logs()
