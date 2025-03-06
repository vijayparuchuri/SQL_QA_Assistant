import yaml
from typing import Dict
import os
from dotenv import load_dotenv

def load_config() -> Dict:
    load_dotenv()

    with open("../config/config.yaml", "r") as file:
        config = yaml.safe_load(file)

    # Replace environment variables in config
    if "database" in config:
        config["database"]["user"] = os.getenv("DB_USER")
        config["database"]["password"] = os.getenv("DB_PASSWORD")

    return config
