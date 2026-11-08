import os
import configparser

class ConfigManager:
    def __init__(self, filepath="config.ini"):
        self.config = configparser.ConfigParser()
        if os.path.exists(filepath):
            self.config.read(filepath, encoding="utf-8")
        else:
            self.config["system"] = {
                "app_title": "IstDigitales Control Center",
                "superadmin_name": "Carlos Arboleda Bernita",
                "version": "1.0.0"
            }
            self.config["api"] = {
                "local_url": "http://localhost:8000",
                "apps_endpoint": "/api/apps/"
            }

    def get(self, section, key, fallback=None):
        try:
            return self.config.get(section, key)
        except Exception:
            return fallback

cfg = ConfigManager()