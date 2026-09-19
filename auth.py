import os
import json
import hashlib
from config import Config

USERS_DB_FILE = os.path.join(os.path.dirname(__file__), "users.json")

class AuthManager:
    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def _load_users() -> dict:
        default_db = {
            "admin": {
                "username": "admin",
                "full_name": "Abdullah Al Naser (Master Admin)",
                "email": "admin@agentnaserseopro.com",
                "password_hash": AuthManager._hash_password("NASER011950"),
                "role": "Admin",
                "plan": "Enterprise Agency"
            },
            "demo": {
                "username": "demo",
                "full_name": "Public Demo Viewer (Read-Only)",
                "email": "demo@agentnaserseopro.com",
                "password_hash": AuthManager._hash_password("demo123"),
                "role": "Demo",
                "plan": "Public Demo Mode"
            }
        }

        if not os.path.exists(USERS_DB_FILE):
            AuthManager._save_users(default_db)
            return default_db

        try:
            with open(USERS_DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "demo" not in data:
                    data["demo"] = default_db["demo"]
                    AuthManager._save_users(data)
                return data
        except Exception as e:
            print(f"[AuthManager] Error loading users db: {e}")
            return default_db

    @staticmethod
    def _save_users(users: dict):
        try:
            with open(USERS_DB_FILE, "w", encoding="utf-8") as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[AuthManager] Error saving users db: {e}")

    @classmethod
    def authenticate(cls, username_or_email: str, password: str) -> tuple:
        """Authenticate user against username or email and password."""
        users = cls._load_users()
        uname_clean = username_or_email.strip().lower()
        pwd_hash = cls._hash_password(password)

        # Check hardcoded master admin fallback
        if (uname_clean == "admin" or uname_clean == "admin@agentnaserseopro.com") and password == "NASER011950":
            return True, {
                "username": "admin",
                "full_name": "Abdullah Al Naser (Master Admin)",
                "email": "admin@agentnaserseopro.com",
                "role": "Admin",
                "plan": "Enterprise Agency"
            }, "Welcome back Master Admin (Abdullah Al Naser)! Full Execution Access Unlocked."

        # Check hardcoded public demo user fallback
        if (uname_clean == "demo" or uname_clean == "demo@agentnaserseopro.com") and (password == "demo123" or password == "demo"):
            return True, {
                "username": "demo",
                "full_name": "Public Demo Viewer (Read-Only)",
                "email": "demo@agentnaserseopro.com",
                "role": "Demo",
                "plan": "Public Demo Mode"
            }, "Welcome Public Viewer! You are in Read-Only Demo Mode. You can view all UI tabs & dashboards."

        for user_key, u_data in users.items():
            if user_key == uname_clean or u_data.get("email", "").lower() == uname_clean:
                if u_data.get("password_hash") == pwd_hash:
                    return True, u_data, f"Welcome back {u_data.get('full_name', uname_clean)}!"
                else:
                    return False, None, "Invalid password. Please check your credentials."

        return False, None, "User account not found. Please register or check username."

    @classmethod
    def register_user(cls, full_name: str, email: str, username: str, password: str, plan: str = "Starter Free") -> tuple:
        """Register a new user in users.json database."""
        users = cls._load_users()
        uname_clean = username.strip().lower()
        email_clean = email.strip().lower()

        if not uname_clean or not password or not email_clean or not full_name:
            return False, "All fields are required for registration."

        if uname_clean in users:
            return False, "Username already exists. Please choose another username."

        for u in users.values():
            if u.get("email", "").lower() == email_clean:
                return False, "Email address is already registered. Please sign in."

        new_user = {
            "username": uname_clean,
            "full_name": full_name.strip(),
            "email": email_clean,
            "password_hash": cls._hash_password(password),
            "role": "User",
            "plan": plan
        }

        users[uname_clean] = new_user
        cls._save_users(users)
        return True, f"Registration successful for {full_name}! You can now sign in."
