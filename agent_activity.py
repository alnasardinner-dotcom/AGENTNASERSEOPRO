import os
import json
from datetime import datetime
from config import Config

ACTIVITY_LOG_FILE = os.path.join(Config.OUTPUT_DIR, "agent_activity.json")

class AgentActivityLogger:
    @staticmethod
    def log_activity(action: str, target: str, status: str = "SUCCESS", details: str = ""):
        """Log 24/7 agent background activities with timestamps."""
        output_dir = Config.OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)

        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "target": target,
            "status": status,
            "details": details
        }

        activities = AgentActivityLogger.get_activities()
        activities.insert(0, entry)  # Prepend newest activity

        # Keep last 100 activity logs
        activities = activities[:100]

        try:
            with open(ACTIVITY_LOG_FILE, "w", encoding="utf-8") as f:
                json.dump(activities, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ActivityLogger] Error logging activity: {e}")

    @staticmethod
    def get_activities() -> list:
        """Fetch all logged 24/7 agent activities."""
        if os.path.exists(ACTIVITY_LOG_FILE):
            try:
                with open(ACTIVITY_LOG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[ActivityLogger] Error reading log file: {e}")
        return []
